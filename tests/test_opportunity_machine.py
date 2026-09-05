from app.services.opportunity_machine import IDEA_FAMILIES, OpportunityMachine

def test_machine_has_many_families():
    assert len(IDEA_FAMILIES) >= 60
    assert "micro_saas" in IDEA_FAMILIES
    assert "export_buyer_hunting" in IDEA_FAMILIES

def test_signal_expands_to_all_families():
    m = OpportunityMachine(max_workers=4)
    items = m.discover({"domain":"ecommerce","problem":"slow conversion","payer":"store","evidence":["audit"],"customer_fit":0.9,"probability":0.6})
    assert len(items) == len(IDEA_FAMILIES)
    assert len(m.create_missions(items)) == len(items)

def test_parallel_execution_isolated_failures():
    m = OpportunityMachine(max_workers=4)
    missions = [{"mission_id":str(i)} for i in range(8)]
    def run(x):
        if x["mission_id"] == "3": raise RuntimeError("expected")
        return x["mission_id"]
    results = m.execute_missions(missions, run)
    assert len(results) == 8
    assert sum(x["status"] == "FAILED" for x in results) == 1
    assert sum(x["status"] == "COMPLETED" for x in results) == 7

def test_learning():
    r = OpportunityMachine.learn([{"status":"COMPLETED"},{"status":"FAILED"},{"status":"COMPLETED"}])
    assert r["completed"] == 2 and r["failed"] == 1

def test_missing_economics_are_not_invented():
    o = OpportunityMachine().discover({"domain":"general","problem":"x"})[0]
    assert o.expected_revenue is None and o.expected_cost is None
