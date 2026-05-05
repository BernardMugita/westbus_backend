from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import get_db

# ─── Auth & Users ─────────────────────────────────────────────────────────────
from app.routers.auth.auth_services import router as auth_router
from app.routers.users.user_services import router as user_router

# ─── Vehicle & Drivers ────────────────────────────────────────────────────────
from app.routers.vehicle.vehicle_services import router as vehicle_router
from app.routers.driver.driver_services import router as driver_router
from app.routers.driver_assignment.driver_assignment_services import router as driver_assignment_router
from app.routers.driver_score_history.driver_score_history_services import router as driver_score_history_router

# # ─── Routes & Trips ───────────────────────────────────────────────────────────
from app.routers.routes.routes_services import router as routes_router
from app.routers.trips.trips_services import router as trips_router

# # ─── Bookings & Seats ─────────────────────────────────────────────────────────
# from app.routers.bookings.bookings_services import router as bookings_router
# from app.routers.seat_allocations.seat_allocations_services import router as seat_allocations_router

# ─── Payments & Revenue ───────────────────────────────────────────────────────
# from app.routers.payments.payments_services import router as payments_router
from app.routers.revenue_ledger.revenue_ledger_services import router as revenue_ledger_router

# ─── Expenses & Loans ─────────────────────────────────────────────────────────
from app.routers.expense.expense_services import router as expense_router
from app.routers.loans.loans_services import router as loans_router
from app.routers.loan_repayments.loan_repayments_services import router as loan_repayments_router

# ─── Maintenance ──────────────────────────────────────────────────────────────
from app.routers.maintenance_records.maintenance_records_services import router as maintenance_records_router
from app.routers.maintenance_schedules.maintenance_schedules_services import router as maintenance_schedules_router

# ─── Insurance ────────────────────────────────────────────────────────────────
from app.routers.insurance_policy.insurance_policy_services import router as insurance_policy_router
from app.routers.insurance_claim.insurance_claim_services import router as insurance_claim_router
from app.routers.dashboard.dashboard_services import router as dashboard_router

app = FastAPI(title="WestBus API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Register Routers ─────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(vehicle_router)
app.include_router(driver_router)
app.include_router(driver_assignment_router)
app.include_router(driver_score_history_router)
app.include_router(routes_router)
app.include_router(trips_router)
app.include_router(revenue_ledger_router)
app.include_router(expense_router)
app.include_router(loans_router)
app.include_router(loan_repayments_router)
app.include_router(maintenance_records_router)
app.include_router(maintenance_schedules_router)
app.include_router(insurance_policy_router)
app.include_router(insurance_claim_router)
app.include_router(dashboard_router)

@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    return {
        "message": "Welcome to the WestBus API!"
    }
