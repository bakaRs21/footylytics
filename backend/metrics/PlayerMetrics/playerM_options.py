from fastapi import APIRouter

metric_options = [
    {
        "key": 'goals_per_match',
        "label": "Player Average Goals per Match",
        "params": [
            {"name": "player_id", 'type': 'int', 'required': False, 'help': 'Filter to one player_id; if skipped return all players'},
            {'name': 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season_id; if skipped return all seasons'},
        ]
    }, {
        "key": 'assists_per_match',
        "label": "Player Average Assists per Match",
        "params": [
            {"name": "player_id", 'type': 'int', 'required': False, 'help': 'Filter to one player_id; if skipped return all players'},
            {'name': 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season_id; if skipped return all seasons'},
        ]
    }, {
        "key": 'shots_per_match',
        "label": "Player Average Shots per Match",
        "params": [
            {"name": "player_id", 'type': 'int', 'required': False, 'help': 'Filter to one player_id; if skipped return all players'},
            {'name': 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season_id; if skipped return all seasons'},
        ]
    }, {
        "key": 'penalty_success_rate',
        "label": "Player Penalty Success Rate",
        "params": [
            {"name": "player_id", 'type': 'int', 'required': False, 'help': 'Filter to one player_id; if skipped return all players'},
            {'name': 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season_id; if skipped return all seasons'},
        ]
    }
]

router = APIRouter(prefix="/player-metrics", tags=["Player Metrics"])
@router.get("/options")
def get_metric_options():
    return metric_options