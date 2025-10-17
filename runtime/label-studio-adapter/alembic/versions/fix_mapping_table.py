"""fix mapping table structure

Revision ID: fix_mapping_table
Revises: remove_unique_constraint
Create Date: 2025-10-14 20:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fix_mapping_table'
down_revision = 'remove_unique_constraint'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. 添加 labelling_project_name 列（如果不存在）
    conn = op.get_bind()
    
    # 检查列是否存在
    result = conn.execute(sa.text("""
        SELECT COUNT(*) 
        FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = 'mapping' 
        AND COLUMN_NAME = 'labelling_project_name'
    """))
    
    count = result.scalar()
    column_exists = count is not None and count > 0
    
    if not column_exists:
        op.add_column('mapping', 
            sa.Column('labelling_project_name', sa.String(255), nullable=True, comment='标注项目名称')
        )
    
    # 2. 移除 source_dataset_id 的唯一约束（如果存在）
    # 查找所有与 source_dataset_id 相关的唯一约束
    result = conn.execute(sa.text("""
        SELECT CONSTRAINT_NAME 
        FROM information_schema.TABLE_CONSTRAINTS 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = 'mapping' 
        AND CONSTRAINT_TYPE = 'UNIQUE'
        AND CONSTRAINT_NAME LIKE '%source%'
    """))
    
    for row in result:
        constraint_name = row[0]
        try:
            op.execute(f"ALTER TABLE mapping DROP INDEX `{constraint_name}`")
        except:
            pass
    
    # 3. 移除可能存在的唯一索引
    result = conn.execute(sa.text("""
        SELECT INDEX_NAME 
        FROM information_schema.STATISTICS 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = 'mapping' 
        AND NON_UNIQUE = 0
        AND INDEX_NAME LIKE '%source%'
        AND INDEX_NAME != 'PRIMARY'
    """))
    
    for row in result:
        index_name = row[0]
        try:
            op.execute(f"ALTER TABLE mapping DROP INDEX `{index_name}`")
        except:
            pass


def downgrade() -> None:
    # 恢复唯一约束
    op.create_index('ix_mapping_source_dataset_id', 'mapping', ['source_dataset_id'], unique=True)
    
    # 删除 labelling_project_name 列
    op.drop_column('mapping', 'labelling_project_name')
