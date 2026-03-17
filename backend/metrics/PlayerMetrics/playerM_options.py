from fastapi import APIRouter

metric_options = [
    {
        "key": "goals_per_match",
        "label": "Player Goals per Match",
        "params": [
            {"name": "player_id", "type": "int", "required": False, "help": "Filter to one player_id; if skipped return all players"},
            {"name": "season_id", "type": "int", "required": False, "help": "Filter to one season_id; if skipped return all seasons"},
        ]
    },
    {
        "key": "assists_per_match",
        "label": "Player Assists per Match",
        "params": [
            {"name": "player_id", "type": "int", "required": False, "help": "Filter to one player_id; if skipped return all players"},
            {"name": "season_id", "type": "int", "required": False, "help": "Filter to one season_id; if skipped return all seasons"},
        ]
    },
    {
        "key": "shots_per_match",
        "label": "Player Shots per Match",
        "params": [
            {"name": "player_id", "type": "int", "required": False, "help": "Filter to one player_id; if skipped return all players"},
            {"name": "season_id", "type": "int", "required": False, "help": "Filter to one season_id; if skipped return all seasons"},
        ]
    },
    {
        "key": "minutes_per_match",
        "label": "Player Minutes per Match",
        "params": [
            {"name": "player_id", "type": "int", "required": False, "help": "Filter to one player_id; if skipped return all players"},
            {"name": "season_id", "type": "int", "required": False, "help": "Filter to one season_id; if skipped return all seasons"},
        ]
    },
    {
        "key": "penalty_success_rate",
        "label": "Player Penalty Success Rate",
        "params": [
            {"name": "player_id", "type": "int", "required": False, "help": "Filter to one player_id; if skipped return all players"},
            {"name": "season_id", "type": "int", "required": False, "help": "Filter to one season_id; if skipped return all seasons"},
        ]
    },
    {
        "key": "shots_accuracy",
        "label": "Player Shots Accuracy",
        "params": [
            {"name": "player_id", "type": "int", "required": False, "help": "Filter to one player_id; if skipped return all players"},
            {"name": "season_id", "type": "int", "required": False, "help": "Filter to one season_id; if skipped return all seasons"},
        ]
    },
    {
        "key": "basic_player_stats",
        "label": "Basic Stats for Player",
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