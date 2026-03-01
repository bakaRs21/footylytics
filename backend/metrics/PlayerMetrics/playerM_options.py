from fastapi import APIRouter

metric_options = [
    {
        "key": "goals_per_match",
        "label": "Player Average Goals per Match",
        "display": {
            "kind": "bar",
            "valueKey": "average_goals_per_match",
            "labelKey": "player_name",
            "unit": "goals",
            "decimals": 3,
            "higherIsBetter": True,
        },
        "params": [
            {"name": "player_id", "type": "int", "required": False, "help": "Filter to one player_id; if skipped return all players"},
            {"name": "season_id", "type": "int", "required": False, "help": "Filter to one season_id; if skipped return all seasons"},
        ]
    },
    {
        "key": "assists_per_match",
        "label": "Player Average Assists per Match",
        "display": {
            "kind": "bar",
            "valueKey": "average_assists_per_match",
            "labelKey": "player_name",
            "unit": "assists",
            "decimals": 3,
            "higherIsBetter": True,
        },
        "params": [
            {"name": "player_id", "type": "int", "required": False, "help": "Filter to one player_id; if skipped return all players"},
            {"name": "season_id", "type": "int", "required": False, "help": "Filter to one season_id; if skipped return all seasons"},
        ]
    },
    {
        "key": "shots_per_match",
        "label": "Player Average Shots per Match",
        "display": {
            "kind": "bar",
            "valueKey": "average_shots_per_match",
            "labelKey": "player_name",
            "unit": "shots",
            "decimals": 3,
            "higherIsBetter": True,
        },
        "params": [
            {"name": "player_id", "type": "int", "required": False, "help": "Filter to one player_id; if skipped return all players"},
            {"name": "season_id", "type": "int", "required": False, "help": "Filter to one season_id; if skipped return all seasons"},
        ]
    },
    {
        "key": "minutes_per_match",
        "label": "Player Average Minutes per Match",
        "display": {
            "kind": "bar",
            "valueKey": "average_minutes_per_match",
            "labelKey": "player_name",
            "unit": "min",
            "decimals": 1,
            "higherIsBetter": True,
        },
        "params": [
            {"name": "player_id", "type": "int", "required": False, "help": "Filter to one player_id; if skipped return all players"},
            {"name": "season_id", "type": "int", "required": False, "help": "Filter to one season_id; if skipped return all seasons"},
        ]
    },
    {
        "key": "penalty_success_rate",
        "label": "Player Penalty Success Rate",
        "display": {
            "kind": "bar",
            "valueKey": "penalty_succes_rate",
            "labelKey": "player_name",
            "unit": "%",
            "decimals": 1,
            "higherIsBetter": True,
        },
        "params": [
            {"name": "player_id", "type": "int", "required": False, "help": "Filter to one player_id; if skipped return all players"},
            {"name": "season_id", "type": "int", "required": False, "help": "Filter to one season_id; if skipped return all seasons"},
        ]
    },
    {
        "key": "shots_accuracy",
        "label": "Player Shots Accuracy",
        "display": {
            "kind": "bar",
            "valueKey": "accuracy_pct",
            "labelKey": "player_name",
            "unit": "%",
            "decimals": 2,
            "higherIsBetter": True,
        },
        "params": [
            {"name": "player_id", "type": "int", "required": False, "help": "Filter to one player_id; if skipped return all players"},
            {"name": "season_id", "type": "int", "required": False, "help": "Filter to one season_id; if skipped return all seasons"},
        ]
    },
    {
        "key": "basic_player_stats",
        "label": "Basic Stats for Player",
        "display": {
            "kind": "table",
        },
        "params": [
            {"name": "player_id", "type": "int", "required": False},
            {"name": "season_id", "type": "int", "required": False}
        ]
    }
]

router = APIRouter(prefix="/player-metrics", tags=["Player Metrics"])

@router.get("/options")
def get_metric_options():
    return metric_options