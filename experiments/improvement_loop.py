import json
import logging
import sqlite3
import numpy as np
from content_creation_agent import create_article_with_params
from param_explorer import evaluate_skill
from skopt import gp_minimize
from skopt.space import Real, Integer, Categorical
from skopt.utils import use_named_args

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = "sen_v3.db"
space = [
    Categorical(['template1', 'template2', 'template3'], name='template_style'),
    Real(0.5, 1.5, name='temperature'),
    Integer(50, 200, name='min_length'),
    Categorical([True, False], name='use_emoji')
]

def save_skill_version(campaign_id, worker_name, params, content, score):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO skill_versions (campaign_id, worker_name, params, content, score) VALUES (?, ?, ?, ?, ?)",
        (campaign_id, worker_name, json.dumps(params), content, score)
    )
    conn.commit()
    conn.close()

def objective(params, campaign_id="mock1"):
    template_style, temperature, min_length, use_emoji = params
    params_dict = {
        'template_style': template_style,
        'temperature': float(temperature),
        'min_length': int(min_length),
        'use_emoji': bool(use_emoji)
    }
    campaign = {
        "campaign_id": campaign_id,
        "name": "Sản phẩm mẫu",
        "commission": 15.0,
        "description": "Mô tả sản phẩm"
    }
    content = create_article_with_params(campaign, params_dict)
    score = evaluate_skill(params_dict, [campaign])
    if isinstance(score, dict):
        score = score.get('total_score', 0)
    score_val = float(score)
    save_skill_version(campaign_id, "content_creator", params_dict, content, score_val)
    logger.info(f"Params: {params_dict} => Score: {score_val}")
    return -score_val

def run_improvement_loop(campaign_id="mock1", n_calls=10):
    @use_named_args(space)
    def objective_wrapper(**params):
        return objective([params['template_style'], params['temperature'], params['min_length'], params['use_emoji']], campaign_id)
    
    res = gp_minimize(
        func=objective_wrapper,
        dimensions=space,
        n_calls=n_calls,
        random_state=42,
        n_initial_points=5
    )
    
    # Lấy giá trị tối ưu
    best_template = str(res.x[0])  # chuyển numpy.str_ thành string
    best_temperature = float(res.x[1])
    best_min_length = int(res.x[2])
    best_use_emoji = bool(res.x[3])
    
    best_params = {
        'template_style': best_template,
        'temperature': best_temperature,
        'min_length': best_min_length,
        'use_emoji': best_use_emoji
    }
    best_score = -float(res.fun)
    logger.info(f"Best params: {best_params}, Best score: {best_score}")
    return best_params, best_score

if __name__ == "__main__":
    best_params, best_score = run_improvement_loop("mock1", n_calls=10)
    print(json.dumps({"best_params": best_params, "best_score": best_score}, indent=2))
