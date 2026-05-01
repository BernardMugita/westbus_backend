import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from app.db.database import engine
from app.routers.core.models import Base
from app.routers.auth.auth_model import User
from app.routers.vehicle.vehicle_model import Vehicle
from app.routers.bookings.bookings_model import Booking
from app.routers.vehicle.vehicle_model import Vehicle
from app.routers.driver.driver_model import Driver
from app.routers.driver_assignment.assignment_model import DriverAssignment
from app.routers.driver_score_history.history_model import DriverScoreHistory
from app.routers.routes.routes_model import Route
from app.routers.trips.trips_model import Trip
from app.routers.bookings.bookings_model import Booking
from app.routers.seat_allocations.seats_model import SeatAllocation
from app.routers.payments.payments_model import Payment
from app.routers.revenue_ledger.ledger_model import RevenueLedger
from app.routers.expense.expenses_model import Expense
from app.routers.loans.loans_model import Loan
from app.routers.loan_repayments.loan_repayments_model import LoanRepayment
from app.routers.maintenance_records.maintenance_model import MaintenanceRecord
from app.routers.maintenance_schedules.schedules_model import MaintenanceSchedule
from app.routers.insurance_policy.policy_model import InsurancePolicy
from app.routers.insurance_claim.claims_model import InsuranceClaim

import asyncio

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
    print("Tables created successfully.")