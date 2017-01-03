import json
import webapp2

from datetime import datetime

from google.appengine.ext import ndb

from controllers.apiv3.api_base_controller import ApiBaseController
from controllers.apiv3.model_properties import team_properties

from database.award_query import TeamAwardsQuery, TeamEventAwardsQuery
from database.event_query import TeamEventsQuery, TeamYearEventsQuery
from database.match_query import TeamEventMatchesQuery
from database.media_query import TeamYearMediaQuery
from database.robot_query import TeamRobotsQuery
from database.team_query import TeamListQuery, TeamParticipationQuery, TeamDistrictsQuery
from helpers.award_helper import AwardHelper
from helpers.model_to_dict import ModelToDict
from helpers.data_fetchers.team_details_data_fetcher import TeamDetailsDataFetcher
from helpers.media_helper import MediaHelper

from models.team import Team


class ApiTeamControllerBase(ApiBaseController):
    @property
    def _validators(self):
        return [("team_id_validator", self.team_key)]

    def _set_team(self, team_key):
        self.team = Team.get_by_id(team_key)
        if self.team is None:
            self._errors = json.dumps({"404": "%s team not found" % team_key})
            self.abort(404)


class ApiTeamListController(ApiTeamControllerBase):
    """
    Returns a JSON list of teams, paginated by team number in sets of 500
    page_num = 0 returns teams from 0-499
    page_num = 1 returns teams from 500-999
    page_num = 2 returns teams from 1000-1499
    etc.
    """
    CACHE_KEY_FORMAT = "apiv3_team_list_controller_{}_{}"  # (page_num, model_type)
    CACHE_VERSION = 1
    CACHE_HEADER_LENGTH = 60 * 60 * 24
    PAGE_SIZE = 500

    def __init__(self, *args, **kw):
        super(ApiTeamListController, self).__init__(*args, **kw)
        self.page_num = self.request.route_kwargs['page_num']
        self.model_type = self.request.route_kwargs.get('model_type')
        self._partial_cache_key = self.CACHE_KEY_FORMAT.format(self.page_num, self.model_type)

    @property
    def _validators(self):
        return []

    def _track_call(self, page_num, model_type=None):
        if model_type:
            self._track_call_defer('team/list/{}'.format(model_type), page_num)
        else:
            self._track_call_defer('team/list', page_num)

    def _render(self, page_num, model_type=None):
        team_list = TeamListQuery(int(page_num)).fetch(dict_version='3')
        if model_type is not None:
            team_list = [{key: team[key] for key in team_properties[model_type]} for team in team_list]
        return json.dumps(team_list, ensure_ascii=True)
