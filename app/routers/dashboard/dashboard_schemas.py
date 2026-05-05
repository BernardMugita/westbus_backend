from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class ComplianceAlert(BaseModel):
    vehicle_id: str
    registration_number: str
    expiry_date: datetime
    type: str  # "License" or "Insurance"

class ActiveClaim(BaseModel):
    claim_id: str
    vehicle_id: str
    registration_number: str
    status: str
    amount_claimed: float

class FinancialSummary(BaseModel):
    total_revenue: float
    total_expenses: float
    net_profit: float

class ChartDataPoint(BaseModel):
    label: str
    revenue: float
    expense: float

class ExpenseCategory(BaseModel):
    category: str
    amount: float

class LoanHealth(BaseModel):
    total_outstanding: float
    next_repayment_date: Optional[datetime]
    next_repayment_amount: Optional[float]

class MaintenanceInsight(BaseModel):
    vehicle_id: str
    registration_number: str
    service_type: str
    due_in_km: Optional[int]
    due_in_days: Optional[int]

class VehicleMaintenanceCost(BaseModel):
    vehicle_id: str
    registration_number: str
    total_cost: float

class RecentTrip(BaseModel):
    trip_id: str
    route: str
    driver: str
    vehicle: str
    status: str
    start_time: datetime
    distance_km: Optional[float]

class RecentRevenue(BaseModel):
    revenue_id: str
    trip_id: str
    amount: float
    source: str
    recorded_at: datetime

class RouteProfitability(BaseModel):
    route_name: str
    revenue: float
    expenses: float
    profit: float

class OperationalKPIs(BaseModel):
    fuel_efficiency: float  # distance / fuel_cost (since we don't have liters)
    fleet_availability: float  # percentage

class FleetStatus(BaseModel):
    total: int
    active: int
    maintenance: int
    expired_docs: int

class DashboardData(BaseModel):
    fleet_status: FleetStatus
    compliance_alerts: List[ComplianceAlert]
    active_claims: List[ActiveClaim]
    financial_summary: FinancialSummary
    revenue_vs_expense: List[ChartDataPoint]
    expense_breakdown: List[ExpenseCategory]
    loan_health: LoanHealth
    maintenance_insights: List[MaintenanceInsight]
    top_maintenance_costs: List[VehicleMaintenanceCost]
    operational_kpis: OperationalKPIs
    recent_trips: List[RecentTrip]
    recent_revenue: List[RecentRevenue]
    route_profitability: List[RouteProfitability]

class DashboardResponse(BaseModel):
    status: str
    message: str
    payload: Optional[DashboardData] = None
