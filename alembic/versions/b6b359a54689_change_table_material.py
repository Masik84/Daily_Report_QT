"""change table Material

Revision ID: b6b359a54689
Revises: 6f2fe6e3e7ce
Create Date: 2025-07-26 19:10:53.342684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6b359a54689'
down_revision: Union[str, None] = '6f2fe6e3e7ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Удалите неверные внешние ключи
    op.drop_constraint('fk_company_plans_abc_category_id_abc_categories', 'company_plans', type_='foreignkey')
    
    # Добавьте правильные внешние ключи
    op.create_foreign_key(
        'fk_company_plans_abc_list_id_abc_list',
        'company_plans', 'abc_list',
        ['abc_list_id'], ['id']
    )

def downgrade():
    op.drop_constraint('fk_company_plans_abc_list_id_abc_list', 'company_plans', type_='foreignkey')
    # Восстановите старую структуру, если нужно

