from fastapi import APIRouter

router = APIRouter(prefix="/team-metrics", tags=["Team Metrics"])

METRIC_OPTIONS = [
    {
        "key": 'goals_scored_per_match',
        "label": "Team Goals per Match",
        "params": [
            {"name": "team_id", 'type': 'int', 'required': False, 'help': 'Filter to one team_id; if skipped return all teams'},
            {'name': 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season_id; if skipped return all seasons'},
        ]
    }, {
        'key': 'goals_conceded_per_match',
        'label': "Team goals conceded per match",
        'params': [
            {'name': 'team_id', 'type': 'int', 'required': False, 'help': 'Filter to one team; if skipped return all teams'},
            {'name': 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season; if skipped return all seasons'}
        ]
    }, {
        "key": "goal_difference_per_match",
        "label": "Team goal difference per match",
        "params": [
            {"name": "team_id", "type": 'int', 'required': False, 'help': 'Filter to one team; if skipped return all teams'},
            {"name": 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season; if skipped return all seasons'}
        ]
    }, {
        "key": "attack_defense_balance",
        "label": "Attack-defense balance (GF - GA)",
        "params": [
            {"name": "team_id", "type": "int", "required": False},
            {"name": "season_id", "type": "int", "required": False},
        ],
    }, {
        "key": "points_per_match",
        "label": "Points per match",
        "params": [
            {"name": "team_id", "type": "int", "required": False},
            {"name": "season_id", "type": "int", "required": False},
        ],
    }, {
        "key": "win_rate",
        "label": "Win rate (%)",
        "params": [
            {"name": "team_id", "type": "int", "required": False},
            {"name": "season_id", "type": "int", "required": False},
        ],
    }, {
        "key": "points_per_goal_scored",
        "label": "Points per goal scored",
        "params": [
            {"name": "team_id", "type": "int", "required": False},
            {"name": "season_id", "type": "int", "required": False},
        ],
    }, {
        "key": "season_consistency_index",
        "label": "Season consistency index ((wins+losses)/matches)",
        "params": [
            {"name": "team_id", "type": "int", "required": False},
            {"name": "season_id", "type": "int", "required": False},
        ],
    }, {
        "key": "goals_scored_percentage_by_minutes",
        "label": "Team goals scored percentage by 15 minutes through match",
        "params": [
            {"name": "team_id", "type": "int", "required": False},
            {"name": "season_id", "type": "int", "required": False}
        ]
    }, {
        "key": "goals_conceded_percentage_by_minutes",
        "label": "Team goals conceded percentage by 15 minutes through match",
        "params": [
            {"name": "team_id", "type": "int", "required": False},
            {"name": "season_id", "type": "int", "required": False}
        ]
    }, {
        "key": "basic_team_stats",
        "label": "Basic team stats",
        "params": [
            {"name": "team_id", "type": "int", "required": True},
            {"name": "season_id", "type": "int", "required": False}
        ]
    }
]

@router.get("/options")
def list_metrics():
    return METRIC_OPTIONS