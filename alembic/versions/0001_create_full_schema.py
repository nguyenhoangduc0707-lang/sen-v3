"""create full initial schema

Revision ID: 0001_create_full_schema
Revises:
Create Date: 2026-05-28 00:00:00.000000
"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '0001_create_full_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(128), nullable=False, unique=True),
        sa.Column('display_name', sa.String(256)),
        sa.Column('email', sa.String(256), unique=True),
        sa.Column('phone', sa.String(50), unique=True),
        sa.Column('password_hash', sa.String(256), nullable=False),
        sa.Column('is_admin', sa.Boolean, nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        'workers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(256), nullable=False, unique=True),
        sa.Column('category', sa.String(128)),
        sa.Column('version', sa.String(64)),
        sa.Column('last_heartbeat', sa.DateTime),
        sa.Column('status', sa.String(64), server_default='IDLE'),
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('task_id', sa.String(128), unique=True),
        sa.Column('category', sa.String(128)),
        sa.Column('worker_name', sa.String(256), nullable=False),
        sa.Column('payload', sa.JSON),
        sa.Column('status', sa.String(32), server_default='PENDING'),
        sa.Column('retries', sa.Integer, server_default='0'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('started_at', sa.DateTime),
        sa.Column('finished_at', sa.DateTime),
        sa.Column('last_error', sa.Text),
        sa.Column('assigned_to', sa.Integer, sa.ForeignKey('users.id')),
    )

    op.create_table(
        'assignments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id'), nullable=False),
        sa.Column('worker_id', sa.Integer, sa.ForeignKey('workers.id'), nullable=False),
        sa.Column('assigned_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('notes', sa.Text),
    )

    op.create_table(
        'commissions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('amount', sa.Float, nullable=False, server_default='0'),
        sa.Column('source', sa.String(256)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        'stealth_data',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('key', sa.String(256), nullable=False, unique=True),
        sa.Column('value', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        'execution_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id')),
        sa.Column('worker_name', sa.String(256)),
        sa.Column('log_level', sa.String(16)),
        sa.Column('message', sa.Text),
        sa.Column('timestamp', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        'dead_letter',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('original_task_id', sa.Integer),
        sa.Column('category', sa.String(128)),
        sa.Column('worker_name', sa.String(256)),
        sa.Column('payload', sa.JSON),
        sa.Column('failure_reason', sa.Text),
        sa.Column('failed_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        'archived_tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('original_task_id', sa.Integer),
        sa.Column('worker_name', sa.String(256)),
        sa.Column('payload', sa.JSON),
        sa.Column('status', sa.String(32)),
        sa.Column('archived_at', sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('archived_tasks')
    op.drop_table('dead_letter')
    op.drop_table('execution_logs')
    op.drop_table('commissions')
    op.drop_table('assignments')
    op.drop_table('tasks')
    op.drop_table('workers')
    op.drop_table('users')
    op.drop_table('stealth_data')
