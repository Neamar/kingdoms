from django.test import TestCase

from kingdom.models import Kingdom, Folk
from mission.models import Mission, MissionGrid, PendingMission
from bargain.models import PendingBargain, PendingBargainKingdom, PendingBargainSharedMission, PendingBargainSharedMissionAffectation


class UnitTest(TestCase):
	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.f = Folk(kingdom=self.k)
		self.f.save()

		self.m = Mission(
			name="Stub mission",
			slug="stub",
			on_resolution="",
			title=self.t,
		)
		self.m.save()

		self.mg = MissionGrid(
			mission=self.m,
		)
		self.mg.save()

		self.pb = PendingBargain()
		self.pb.save()
