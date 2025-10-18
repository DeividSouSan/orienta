from datetime import datetime, timezone
from src.models import guide


class TestGuideModel:
    def test_generate_with_valid_data(self):
        study_plan = guide.generate("""
    <INPUTS>
        <TOPIC>Fotossíntese</TOPIC>
        <OBJECTIVE>Entender o que acontece antes, durante e depois da fotossíntese e sua importância.</OBJECTIVE>
        <DAILY_DEDICATION_IN_MINUTES>60 minutes</DAILY_DEDICATION_IN_MINUTES>
        <DURATION_IN_DAYS>3 days</DURATION_IN_DAYS>
        <KNOWLEDGE>Biologia do Ensino Médio.</KNOWLEDGE>
    </INPUTS>
        """)

        assert isinstance(study_plan, list)
        assert len(study_plan) == 3

        for day, daily_plan in enumerate(study_plan, start=1):
            assert daily_plan.day == day
            assert daily_plan.title
            assert daily_plan.goal
            assert isinstance(daily_plan.theoretical_research, list)
            assert len(daily_plan.theoretical_research) >= 2
            assert daily_plan.practical_activity
            assert daily_plan.learning_verification

    def test_build_with_valid_data(self):
        guide_info: guide.GuideInfo = guide.build(
            uid="123",
            inputs={
                "topic": "Fotossíntese",
                "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância",
                "study_time": "60",
                "duration_time": "3",
                "knowledge": "Biologia do Ensino Médio",
            },
        )

        assert isinstance(guide_info["uid"], str)
        assert isinstance(guide_info["inputs"], dict)
        assert guide_info["model"] == "gemini-2.0-flash-lite"
        assert guide_info["temperature"] == 2
        assert isinstance(guide_info["generation_time_ms"], int)
        assert guide_info["generation_time_ms"] > 0
        assert isinstance(guide_info["daily_study"], list)

    def test_find_guides_with_user_with_no_guides(self):
        guides = guide.find_guides("9999")

        assert isinstance(guides, list)
        assert len(guides) == 0

    def test_find_guides_with_user_with_one_guide(self):
        result = guide.GuideInfo = guide.build(
            uid="1234",
            inputs={
                "topic": "Fotossíntese",
                "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância",
                "study_time": "60",
                "duration_time": "3",
                "knowledge": "Biologia do Ensino Médio",
            },
        )

        guide.save(result)
        guides = guide.find_guides("1234")

        print("Guias: ", guides)
        assert isinstance(guides, list)
        assert len(guides) >= 1

        assert guides[0]["id"]
        assert guides[0]["topic"] == "Fotossíntese"
        assert (
            guides[0]["objective"]
            == "Entender o que acontece antes, durante e depois da fotossíntese e sua importância"
        )
        assert guides[0]["duration"] == "3"
        assert guides[0]["created_at"] == guide.format_date(
            datetime.now(tz=timezone.utc)
        )

    def test_retrieve_daily_plan_with_user_with_one_guide(self):
        result = guide.GuideInfo = guide.build(
            uid="4321",
            inputs={
                "topic": "Fotossíntese",
                "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância",
                "study_time": "60",
                "duration_time": "3",
                "knowledge": "Biologia do Ensino Médio",
            },
        )

        guide.save(result)
        guides = guide.find_guides("4321")

        id = guides[0]["id"]
        daily_plan = guide.retrieve_daily_plan(id)

        assert isinstance(daily_plan, list)
        assert len(daily_plan) == 3
