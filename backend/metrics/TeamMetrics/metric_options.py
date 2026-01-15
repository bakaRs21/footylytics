from fastapi import APIRouter

router = APIRouter(prefix="/team-metrics", tags=["Team Metrics"])

METRIC_OPTIONS = [
    {
        "key": 'team_goals_per_match',
        "label": "Team Avarage Goals per Match",
        "params": [
            {"name": "team_id", 'tpye': 'int', 'required': False, 'help': 'Filter to one team_id; if skipped return all teams'},
            {'name': 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season_id; if skipped return all seasons'},
        ]
    },{
        "key": "team_goal_difference",
        "label": "team goal difference ",
        "params": [
            {"name": "team_id", "type": 'int', 'required': False, 'help': 'Filter to one team; if skipped return all teams'},
            {"name": 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season; if skipped return all seasons'}
        ]
    }, {
        'key': 'team_goals_conceded_per_match',
        'label': "Team goals conceded per match",
        'params': [
            {'name': 'team_id', 'type': 'int', 'required': False, 'help': 'Filter to one team; if skipped return all teams'},
            {'name': 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season; if skipped return all seasons'}
        ]
    },{
        "key": "attack_defense_balance",
        "label": "Attack-defense balance (GF - GA)",
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
        "key": "points_per_goal_scored",
        "label": "Points per goal scored",
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
        "key": "points_per_match",
        "label": "Points per match",
        "params": [
            {"name": "team_id", "type": "int", "required": False},
            {"name": "season_id", "type": "int", "required": False},
        ],
    },
]

@router.get("/options")
def list_metrics():
    return METRIC_OPTIONS