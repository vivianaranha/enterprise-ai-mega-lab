from backend.app.agents.super_agent import super_agent

def test_sales_routing():
    route,_=super_agent.route("Find the best sales opportunities")
    assert route=="sales"

def test_support_routing():
    route,_=super_agent.route("Which support tickets broke SLA?")
    assert route=="support"

def test_operations_routing():
    route,_=super_agent.route("Which inventory items might stockout?")
    assert route=="operations"

def test_executive_routing():
    route,_=super_agent.route("Give me an executive brief across the business")
    assert route=="executive"
