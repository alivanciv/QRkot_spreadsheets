from typing import Optional, Union

from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.services.utils import time_format


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, Union[str, int]]]:
        db_projects = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(True))
            .order_by(
                (extract('year', CharityProject.close_date) -
                 extract('year', CharityProject.create_date)),
                (extract('month', CharityProject.close_date) -
                 extract('month', CharityProject.create_date)),
                (extract('day', CharityProject.close_date) -
                 extract('day', CharityProject.create_date)),
                (extract('hour', CharityProject.close_date) -
                 extract('hour', CharityProject.create_date)),
                (extract('minute', CharityProject.close_date) -
                 extract('minute', CharityProject.create_date)),
                (extract('second', CharityProject.close_date) -
                 extract('second', CharityProject.create_date)),
            )
        )
        db_projects = db_projects.scalars().all()
        return [
            {
                'name': project.name,
                'accumulation_time': time_format(
                    project.close_date - project.create_date
                ),
                'description': project.description
            }
            for project in db_projects
        ]


charity_project_crud = CRUDCharityProject(CharityProject)
