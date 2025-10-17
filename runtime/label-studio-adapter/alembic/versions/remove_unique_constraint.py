"""remove unique constraint from source_dataset_id and rename table

Revision ID: remove_unique_constraint
Revises: 1597600460eb
Create Date: 2025-10-14 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'remove_unique_constraint'
down_revision = '1597600460eb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. 重命名表
    op.rename_table('dataset_mappings', 'mapping')
    
    # 2. 重命名列
    op.alter_column('mapping', 'source_dataset_uuid',
                    new_column_name='source_dataset_id',
                    existing_type=sa.String(36),
                    existing_nullable=False)
    
    op.alter_column('mapping', 'labelling_dataset_uuid',
                    new_column_name='labelling_project_id',
                    existing_type=sa.String(36),
                    existing_nullable=False)
    
    # 3. 添加新列
    op.add_column('mapping', sa.Column('labelling_project_name', sa.String(255), nullable=True, comment='标注项目名称'))
    
    # 4. 移除 source_dataset_id 的唯一约束
    # MySQL
    try:
        op.drop_constraint('source_dataset_uuid', 'mapping', type_='unique')
    except:
        pass
    
    # 或者尝试移除索引（如果是通过索引实现的唯一约束）
    try:
        op.drop_index('ix_dataset_mappings_source_dataset_uuid', 'mapping')
    except:
        pass


def downgrade() -> None:
    # 1. 恢复唯一约束
    op.create_unique_constraint('source_dataset_uuid', 'mapping', ['source_dataset_id'])
    
    # 2. 删除新列
    op.drop_column('mapping', 'labelling_project_name')
    
    # 3. 恢复列名
    op.alter_column('mapping', 'labelling_project_id',
                    new_column_name='labelling_dataset_uuid',
                    existing_type=sa.String(36),
                    existing_nullable=False)
    
    op.alter_column('mapping', 'source_dataset_id',
                    new_column_name='source_dataset_uuid',
                    existing_type=sa.String(36),
                    existing_nullable=False)
    
    # 4. 恢复表名
    op.rename_table('mapping', 'dataset_mappings')
