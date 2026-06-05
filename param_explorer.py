import logging
from skopt import gp_minimize
from skopt.space import Real, Integer, Categorical
from skopt.utils import use_named_args
from content_creation_agent import create_article_with_params
from grader import Grader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock data (không cần database)
MOCK_CAMPAIGNS = [
    {"campaign_id": "mock1", "name": "Thời trang mùa hè", "commission": 12.5},
    {"campaign_id": "mock2", "name": "Điện thoại thông minh", "commission": 8.0},
    {"campaign_id": "mock3", "name": "Mỹ phẩm Hàn Quốc", "commission": 15.0}
]

# Không gian tham số cần tối ưu
space = [
    Categorical(['template1', 'template2', 'template3'], name='template_style'),
    Real(0.5, 1.5, name='temperature'),
    Integer(50, 200, name='min_length'),
    Categorical([True, False], name='use_emoji')
]

def evaluate_skill(params, campaigns):
    expectations = [
        {"text": "Có link affiliate", "regex": r"https?://"},
        {"text": "Độ dài > 30", "min_length": 30},
        {"text": "Có từ 'hoa hồng'", "regex": r"hoa hồng"},
        {"text": "Có emoji", "regex": r"[🌟🔥🎯💥]"},
        {"text": "Có kêu gọi hành động", "regex": r"mua ngay|đăng ký"}
    ]
    grader = Grader(expectations)
    total = 0.0
    for camp in campaigns:
        article = create_article_with_params(camp, params)
        grade = grader.grade(article)
        total += grade["summary"]["pass_rate"]
    return -total / len(campaigns)

@use_named_args(space)
def objective(**params):
    logger.info(f"Thử nghiệm: {params}")
    loss = evaluate_skill(params, MOCK_CAMPAIGNS)
    logger.info(f"Điểm trung bình đạt được: {-loss:.2f}")
    return loss

def run_optimization(n_calls=15):
    logger.info("Bắt đầu tối ưu tham số...")
    res = gp_minimize(objective, space, n_calls=n_calls, random_state=42)
    best = {dim.name: res.x[i] for i, dim in enumerate(space)}
    best_score = -res.fun
    logger.info(f"Tham số tối ưu: {best}")
    logger.info(f"Điểm số tốt nhất: {best_score:.2f}")
    return best

if __name__ == "__main__":
    run_optimization()