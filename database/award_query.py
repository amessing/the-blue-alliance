from google.appengine.ext import ndb

from database.database_query import DatabaseQuery
from helpers.model_to_dict import ModelToDict
from models.award import Award
from models.event import Event
from models.team import Team


class EventAwardsQuery(DatabaseQuery):
    CACHE_VERSION = 0
    CACHE_KEY_FORMAT = 'event_awards_{}'  # (event_key)

    @ndb.tasklet
    def _query_async(self, dict_version):
        event_key = self._query_args[0]
        awards = yield Award.query(Award.event == ndb.Key(Event, event_key)).fetch_async()
        if dict_version:
            awards = ModelToDict.convertAwards(awards, dict_version)
        raise ndb.Return(awards)


class TeamAwardsQuery(DatabaseQuery):
    CACHE_VERSION = 0
    CACHE_KEY_FORMAT = 'team_awards_{}'  # (team_key)

    @ndb.tasklet
    def _query_async(self, dict_version):
        team_key = self._query_args[0]
        awards = yield Award.query(
            Award.team_list == ndb.Key(Team, team_key)).fetch_async()
        if dict_version:
            awards = ModelToDict.convertAwards(awards, dict_version)
        raise ndb.Return(awards)


class TeamYearAwardsQuery(DatabaseQuery):
    CACHE_VERSION = 0
    CACHE_KEY_FORMAT = 'team_year_awards_{}_{}'  # (team_key, year)

    @ndb.tasklet
    def _query_async(self, dict_version):
        team_key = self._query_args[0]
        year = self._query_args[1]
        awards = yield Award.query(
            Award.team_list == ndb.Key(Team, team_key),
            Award.year == year).fetch_async()
        if dict_version:
            awards = ModelToDict.convertAwards(awards, dict_version)
        raise ndb.Return(awards)


class TeamEventAwardsQuery(DatabaseQuery):
    CACHE_VERSION = 0
    CACHE_KEY_FORMAT = 'team_event_awards_{}_{}'  # (team_key, event_key)

    @ndb.tasklet
    def _query_async(self, dict_version):
        team_key = self._query_args[0]
        event_key = self._query_args[1]
        awards = yield Award.query(
            Award.team_list == ndb.Key(Team, team_key),
            Award.event == ndb.Key(Event, event_key)).fetch_async()
        if dict_version:
            awards = ModelToDict.convertAwards(awards, dict_version)
        raise ndb.Return(awards)
