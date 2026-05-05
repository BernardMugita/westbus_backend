from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta, timezone

from app.routers.vehicle.vehicle_model import Vehicle, VehicleStatus
from app.routers.insurance_policy.policy_model import InsurancePolicy
from app.routers.insurance_claim.claims_model import InsuranceClaim, ClaimStatus
from app.routers.expense.expenses_model import Expense, ExpenseType
from app.routers.revenue_ledger.ledger_model import RevenueLedger
from app.routers.loans.loans_model import Loan
from app.routers.loan_repayments.loan_repayments_model import LoanRepayment
from app.routers.maintenance_schedules.schedules_model import MaintenanceSchedule
from app.routers.maintenance_records.maintenance_model import MaintenanceRecord
from app.routers.trips.trips_model import Trip
from app.routers.driver.driver_model import Driver
from app.routers.routes.routes_model import Route
from app.routers.dashboard.dashboard_schemas import (
    DashboardResponse, DashboardData, FleetStatus, ComplianceAlert,
    ActiveClaim, FinancialSummary, ChartDataPoint, ExpenseCategory,
    LoanHealth, MaintenanceInsight, VehicleMaintenanceCost, OperationalKPIs,
    RecentTrip, RecentRevenue, RouteProfitability
)
from app.config.core.middlewares import requires_auth, requires_admin

EAT = timezone(timedelta(hours=3))

class DashboardController:
    def __init__(self):
        pass

    @requires_admin
    async def get_dashboard_data(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> DashboardResponse:
        try:
            now = datetime.now(EAT)
            thirty_days_later = now + timedelta(days=30)

            # 1. Fleet Status
            vehicles_result = await db.execute(select(Vehicle))
            vehicles = vehicles_result.scalars().all()
            total_vehicles = len(vehicles)
            active_vehicles = sum(1 for v in vehicles if v.status == VehicleStatus.ACTIVE)
            maintenance_vehicles = sum(1 for v in vehicles if v.status == VehicleStatus.MAINTENANCE)
            
            # 2. Compliance Alerts (Expiries in next 30 days)
            compliance_alerts = []
            for v in vehicles:
                if v.license_expiry and v.license_expiry <= thirty_days_later:
                    compliance_alerts.append(ComplianceAlert(
                        vehicle_id=v.vehicle_id,
                        registration_number=v.registration_number,
                        expiry_date=v.license_expiry,
                        type="License"
                    ))
            
            insurance_result = await db.execute(
                select(InsurancePolicy, Vehicle.registration_number)
                .join(Vehicle, InsurancePolicy.vehicle_id == Vehicle.vehicle_id)
                .where(InsurancePolicy.end_date <= thirty_days_later)
            )
            for policy, reg in insurance_result.all():
                compliance_alerts.append(ComplianceAlert(
                    vehicle_id=policy.vehicle_id,
                    registration_number=reg,
                    expiry_date=policy.end_date,
                    type="Insurance"
                ))
            
            expired_docs_count = len(set(a.vehicle_id for a in compliance_alerts if a.expiry_date <= now))

            # 3. Active Claims
            claims_result = await db.execute(
                select(InsuranceClaim, Vehicle.registration_number, Vehicle.vehicle_id)
                .join(InsurancePolicy, InsuranceClaim.insurance_id == InsurancePolicy.insurance_id)
                .join(Vehicle, InsurancePolicy.vehicle_id == Vehicle.vehicle_id)
                .where(InsuranceClaim.status == ClaimStatus.PENDING)
            )
            active_claims = [
                ActiveClaim(
                    claim_id=c.claim_id,
                    vehicle_id=vid,
                    registration_number=reg,
                    status=c.status.value,
                    amount_claimed=float(c.amount_claimed)
                ) for c, reg, vid in claims_result.all()
            ]

            # 4. Financial Summary
            revenue_sum = await db.execute(select(func.sum(RevenueLedger.amount)))
            total_revenue = float(revenue_sum.scalar() or 0)

            expense_sum = await db.execute(select(func.sum(Expense.amount)))
            total_expenses = float(expense_sum.scalar() or 0)

            # 5. Expense Breakdown
            expense_cats = await db.execute(
                select(Expense.type, func.sum(Expense.amount))
                .group_by(Expense.type)
            )
            expense_breakdown = [
                ExpenseCategory(category=t.value, amount=float(s))
                for t, s in expense_cats.all()
            ]

            # 6. Revenue vs Expense Chart (Last 6 months)
            chart_data = []
            for i in range(5, -1, -1):
                month_start = (now.replace(day=1) - timedelta(days=i*30)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                next_month = (month_start + timedelta(days=32)).replace(day=1)
                
                m_rev = await db.execute(select(func.sum(RevenueLedger.amount)).where(and_(RevenueLedger.recorded_at >= month_start, RevenueLedger.recorded_at < next_month)))
                m_exp = await db.execute(select(func.sum(Expense.amount)).where(and_(Expense.created_at >= month_start, Expense.created_at < next_month)))
                
                chart_data.append(ChartDataPoint(
                    label=month_start.strftime("%b %Y"),
                    revenue=float(m_rev.scalar() or 0),
                    expense=float(m_exp.scalar() or 0)
                ))

            # 7. Loan Health
            loans_result = await db.execute(select(Loan))
            loans = loans_result.scalars().all()
            total_payable = sum(loan.total_payable for loan in loans)
            
            repayments_sum = await db.execute(select(func.sum(LoanRepayment.amount_paid)))
            total_paid = repayments_sum.scalar() or 0
            
            total_outstanding = float(total_payable - total_paid)
            
            # Simple heuristic for next repayment (next month for active loans)
            next_repayment_date = now + timedelta(days=30) # Placeholder logic
            next_repayment_amount = sum(float(loan.monthly_installment) for loan in loans if loan.status == "Active")

            # 8. Maintenance Insights
            maintenance_schedules_result = await db.execute(
                select(MaintenanceSchedule, Vehicle.registration_number)
                .join(Vehicle, MaintenanceSchedule.vehicle_id == Vehicle.vehicle_id)
                .where(MaintenanceSchedule.status != "Done")
            )
            maintenance_insights = [
                MaintenanceInsight(
                    vehicle_id=s.vehicle_id,
                    registration_number=reg,
                    service_type=s.service_type,
                    due_in_km=s.interval_km - (s.last_done_km or 0), # Simplified
                    due_in_days=s.interval_days - (now - s.last_done_date).days if s.last_done_date else s.interval_days
                ) for s, reg in maintenance_schedules_result.all()
            ]

            top_maintenance_costs_result = await db.execute(
                select(Vehicle.vehicle_id, Vehicle.registration_number, func.sum(MaintenanceRecord.cost))
                .join(MaintenanceRecord, Vehicle.vehicle_id == MaintenanceRecord.vehicle_id)
                .group_by(Vehicle.vehicle_id, Vehicle.registration_number)
                .order_by(func.sum(MaintenanceRecord.cost).desc())
                .limit(5)
            )
            top_maintenance_costs = [
                VehicleMaintenanceCost(
                    vehicle_id=vid,
                    registration_number=reg,
                    total_cost=float(cost)
                ) for vid, reg, cost in top_maintenance_costs_result.all()
            ]

            # 9. Operational KPIs
            total_distance_result = await db.execute(select(func.sum(Trip.distance_km)))
            total_distance = float(total_distance_result.scalar() or 0)
            
            fuel_expenses_result = await db.execute(select(func.sum(Expense.amount)).where(Expense.type == ExpenseType.FUEL))
            total_fuel_cost = float(fuel_expenses_result.scalar() or 0)
            
            fuel_efficiency = total_distance / total_fuel_cost if total_fuel_cost > 0 else 0
            fleet_availability = (active_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0

            # 10. Recent Trips
            recent_trips_result = await db.execute(
                select(Trip, Route.route_name, Driver.name, Vehicle.registration_number)
                .join(Route, Trip.route_id == Route.route_id)
                .join(Driver, Trip.driver_id == Driver.driver_id)
                .join(Vehicle, Trip.vehicle_id == Vehicle.vehicle_id)
                .order_by(Trip.start_time.desc())
                .limit(5)
            )
            recent_trips = [
                RecentTrip(
                    trip_id=t.trip_id,
                    route=r_name,
                    driver=d_name,
                    vehicle=v_reg,
                    status=t.status.value,
                    start_time=t.start_time,
                    distance_km=float(t.distance_km) if t.distance_km else None
                ) for t, r_name, d_name, v_reg in recent_trips_result.all()
            ]

            # 11. Recent Revenue
            recent_revenue_result = await db.execute(
                select(RevenueLedger)
                .order_by(RevenueLedger.recorded_at.desc())
                .limit(5)
            )
            recent_revenue = [
                RecentRevenue(
                    revenue_id=r.revenue_id,
                    trip_id=r.trip_id,
                    amount=float(r.amount),
                    source=r.revenue_source.value,
                    recorded_at=r.recorded_at
                ) for r in recent_revenue_result.scalars().all()
            ]

            # 12. Route Profitability
            # Join Trip with Revenue and Expense, grouped by Route
            routes_profit_query = await db.execute(
                select(Route.route_name, func.sum(RevenueLedger.amount).label("rev"), func.sum(Expense.amount).label("exp"))
                .join(Trip, Trip.route_id == Route.route_id)
                .join(RevenueLedger, RevenueLedger.trip_id == Trip.trip_id, isouter=True)
                .join(Expense, Expense.trip_id == Trip.trip_id, isouter=True)
                .group_by(Route.route_name)
            )
            route_profitability = [
                RouteProfitability(
                    route_name=name,
                    revenue=float(rev or 0),
                    expenses=float(exp or 0),
                    profit=float((rev or 0) - (exp or 0))
                ) for name, rev, exp in routes_profit_query.all()
            ]

            dashboard_data = DashboardData(
                fleet_status=FleetStatus(
                    total=total_vehicles,
                    active=active_vehicles,
                    maintenance=maintenance_vehicles,
                    expired_docs=expired_docs_count
                ),
                compliance_alerts=compliance_alerts,
                active_claims=active_claims,
                financial_summary=FinancialSummary(
                    total_revenue=total_revenue,
                    total_expenses=total_expenses,
                    net_profit=total_revenue - total_expenses
                ),
                revenue_vs_expense=chart_data,
                expense_breakdown=expense_breakdown,
                loan_health=LoanHealth(
                    total_outstanding=total_outstanding,
                    next_repayment_date=next_repayment_date,
                    next_repayment_amount=next_repayment_amount
                ),
                maintenance_insights=maintenance_insights,
                top_maintenance_costs=top_maintenance_costs,
                operational_kpis=OperationalKPIs(
                    fuel_efficiency=fuel_efficiency,
                    fleet_availability=fleet_availability
                ),
                recent_trips=recent_trips,
                recent_revenue=recent_revenue,
                route_profitability=route_profitability
            )

            return DashboardResponse(status="success", message="Dashboard data retrieved successfully", payload=dashboard_data)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=DashboardResponse(status="error", message=str(e)).model_dump())
