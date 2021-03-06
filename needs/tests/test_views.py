from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from needs.models import Need, Goal, Step, Iteration, Delivery
from needs.serializers import NeedSerializer
from rest_framework.parsers import JSONParser
import io
import datetime
from django.urls import reverse


class NeedViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'root1', 'email1@exemple.com', 'root')
        self.user2 = User.objects.create_user(
            'root2', 'email2@exemple.com', 'root')

        self.need1 = Need.objects.create(
            name='need1', description='need1 description', user=self.user1)
        self.need2 = Need.objects.create(
            name='need2', description='need2 description', user=self.user1)
        self.need3 = Need.objects.create(
            name='need3', description='need3 description', user=self.user2)

# ==============================================test_need_create==========================================

    def test_need_create(self):
        count = Need.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.post(reverse('needs:need_list'),
                               {
            'name': 'newNeed',
            'description': 'newneedDescription',
        }, format='json')
        self.assertEqual(response.status_code, 201)

        count = Need.objects.all().count()
        self.assertEqual(count, 4)

        need = Need.objects.get(id=4)
        self.assertEqual(need.description, 'newneedDescription')
        self.assertEqual(need.name, 'newNeed')
        self.assertEqual(need.user, self.user1)

    def test_need_create_no_loged_user(self):
        count = Need.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        response = client.post(reverse('needs:need_list'),
                               {
            'name': 'newNeed',
            'description': 'newneedDescription',
        }, format='json')
        self.assertEqual(response.status_code, 401)

        count = Need.objects.all().count()
        self.assertEqual(count, 3)

    def test_need_create_with_icon(self):
        count = Need.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.post(reverse('needs:need_list'),
                               {
            'name': 'newNeed',
            'description': 'newneedDescription',
            'iconName': 'far fa-heart',
            'iconColor': 'bg-red-500',
        }, format='json')
        self.assertEqual(response.status_code, 201)

        count = Need.objects.all().count()
        self.assertEqual(count, 4)

        need = Need.objects.get(id=4)
        self.assertEqual(need.description, 'newneedDescription')
        self.assertEqual(need.name, 'newNeed')
        self.assertEqual(need.user, self.user1)
        self.assertEqual(need.iconName, 'far fa-heart')
        self.assertEqual(need.iconColor, 'bg-red-500')

    # ==============================================test_need_list==========================================

    def test_need_list(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(reverse('needs:need_list'))

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

    def test_need_list_no_loged_user(self):
        client = APIClient()
        response = client.get(reverse('needs:need_list'))

        self.assertEqual(response.status_code, 401)

    # ==============================================test_need_retrieve======================================

    def test_need_retrieve(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(reverse('needs:need_detail', kwargs={'pk': 2}))

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['name'], 'need2')
        self.assertEqual(data['description'], 'need2 description')

    def test_need_retrieve_no_loged_user(self):
        client = APIClient()
        response = client.get(reverse('needs:need_detail', kwargs={'pk': 2}))

        self.assertEqual(response.status_code, 401)

    def test_need_retrieve_other_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(reverse('needs:need_detail', kwargs={'pk': 3}))

        self.assertEqual(response.status_code, 403)

    # ==============================================test_need_update========================================

    def test_need_update(self):
        count = Need.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.put(reverse('needs:need_detail', kwargs={'pk': 2}),
                              {
            'name': 'need2Updated',
            'description': 'need2DescriptionUpdated',
            'iconName': 'far fa-heart',
            'iconColor': 'bg-red-500',
        }, format='json')

        self.assertEqual(response.status_code, 200)
        need = Need.objects.get(id=2)
        self.assertEqual(need.name, 'need2Updated')
        self.assertEqual(need.description, 'need2DescriptionUpdated')
        self.assertEqual(need.iconName, 'far fa-heart')
        self.assertEqual(need.iconColor, 'bg-red-500')
        count = Need.objects.all().count()
        self.assertEqual(count, 3)

    def test_need_update_no_loged_user(self):
        client = APIClient()
        response = client.put(reverse('needs:need_detail', kwargs={'pk': 2}),
                              {
            'name': 'need2Updated',
            'description': 'need2DescriptionUpdated',
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_need_update_other_user(self):
        count = Need.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.put(reverse('needs:need_detail', kwargs={'pk': 3}),
                              {
            'name': 'need2Updated',
            'description': 'need2DescriptionUpdated',
        }, format='json')

        self.assertEqual(response.status_code, 403)
    # ==============================================test_need_delete=======================================

    def test_need_delete(self):
        count = Need.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.delete(
            reverse('needs:need_detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 204)

        count = Need.objects.all().count()
        self.assertEqual(count, 2)

    def test_need_delete_no_loged_user(self):
        count = Need.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        response = client.delete(
            reverse('needs:need_detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 401)

    def test_need_delete_from_other_user(self):
        count = Need.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.delete(
            reverse('needs:need_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 403)

        count = Need.objects.all().count()
        self.assertEqual(count, 3)


class GoalViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'root1', 'email1@exemple.com', 'root')
        self.user2 = User.objects.create_user(
            'root2', 'email2@exemple.com', 'root')

        self.need1 = Need.objects.create(
            name='need1', description='need1 description', user=self.user1)
        self.need2 = Need.objects.create(
            name='need2', description='need2 description', user=self.user1)
        self.need3 = Need.objects.create(
            name='need3', description='need3 description', user=self.user2)

        self.today = datetime.date.today()
        self.goal1 = Goal.objects.create(name="goal1", description='goal1Description',
                                         endDate=self.today, need=self.need1)
        self.goal2 = Goal.objects.create(name="goal2", description='goal2Description',
                                         endDate=self.today, need=self.need1)
        self.goal3 = Goal.objects.create(name="goal3", description='goal3Description',
                                         endDate=self.today, need=self.need3)

    # ==============================================test_goal_create=======================================

    def test_goal_create(self):
        count = Goal.objects.all().count()
        self.assertEqual(count, 3)
        endDate = datetime.date.today()

        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.post(reverse('needs:goal_list'), {
            'name': 'newGoal',
            'description': 'newGoalDescription',
            'endDate': endDate,
            'need': self.need1.id,
        }, format='json')

        self.assertEqual(response.status_code, 201)

        count = Goal.objects.all().count()
        self.assertEqual(count, 4)

        goal = Goal.objects.get(id=4)
        self.assertEqual(goal.name, 'newGoal')
        self.assertEqual(goal.description, 'newGoalDescription')
        self.assertEqual(goal.endDate, endDate)
        self.assertEqual(goal.need, self.need1)

    def test_goal_create_name_length_50(self):
        count = Goal.objects.all().count()
        self.assertEqual(count, 3)
        endDate = datetime.date.today()

        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.post(reverse('needs:goal_list'), {
            'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'description': 'newGoalDescription',
            'endDate': endDate,
            'need': self.need1.id,
        }, format='json')

        self.assertEqual(response.status_code, 201)

        count = Goal.objects.all().count()
        self.assertEqual(count, 4)

        goal = Goal.objects.get(id=4)
        self.assertEqual(goal.name, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.assertEqual(goal.description, 'newGoalDescription')
        self.assertEqual(goal.endDate, endDate)
        self.assertEqual(goal.need, self.need1)

    def test_goal_create_no_loged_user(self):
        count = Goal.objects.all().count()
        self.assertEqual(count, 3)
        endDate = datetime.date.today()

        client = APIClient()
        response = client.post(reverse('needs:goal_list'), {
            'name': 'newGoal',
            'description': 'newGoalDescription',
            'endDate': endDate,
            'need': self.need1.id,
        }, format='json')

        self.assertEqual(response.status_code, 401)

        count = Goal.objects.all().count()
        self.assertEqual(count, 3)

    # ==============================================test_goal_retrieve=======================================

    def test_goal_retrieve(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(reverse('needs:goal_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['name'], 'goal1')
        self.assertEqual(data['description'], 'goal1Description')
        self.assertEqual(data['endDate'], self.today.strftime('%Y-%m-%d'))
        self.assertEqual(data['need']['id'], self.need1.id)
        self.assertEqual(data['need']['name'], self.need1.name)

    def test_goal_retrieve_no_loged_user(self):
        client = APIClient()
        response = client.get(reverse('needs:goal_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 401)

    def test_goal_retrieve_from_other_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get('/goal/3/')
        self.assertEqual(response.status_code, 403)

    # ==============================================test_goal_list=======================================

    def test_goal_list(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(reverse('needs:goal_list'))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 2)

    def test_goal_list_no_loged_user(self):
        client = APIClient()
        response = client.get(reverse('needs:goal_list'))
        self.assertEqual(response.status_code, 401)

    def test_goal_list_by_need(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(
            reverse('needs:goal_list_by_need', kwargs={'need': 1}))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 2)

        self.goal2 = Goal.objects.create(name="goal2", description='goal2Description',
                                         endDate=self.today, need=self.need2)

        response = client.get(
            reverse('needs:goal_list_by_need', kwargs={'need': 1}))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 2)

    # ==============================================test_goal_update=======================================

    def test_goal_update(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.put(reverse('needs:goal_detail', kwargs={'pk': 1}), {
            'name': 'newNameForGoal1',
            'description': 'newDescriptionForGoal1',
            'endDate': self.today,
            'need': self.need2.id,
        }, format='json')

        self.assertEqual(response.status_code, 200)
        goal = Goal.objects.get(id=1)
        self.assertEqual(goal.name, 'newNameForGoal1')
        self.assertEqual(goal.description, 'newDescriptionForGoal1')
        self.assertEqual(goal.endDate, self.today)
        self.assertEqual(goal.need, self.need2)

    def test_goal_update_no_loged_user(self):
        client = APIClient()
        response = client.put(reverse('needs:goal_detail', kwargs={'pk': 1}), {
            'name': 'newNameForGoal1',
            'description': 'newDescriptionForGoal1',
            'endDate': self.today,
            'need': self.need2.id,
        }, format='json')

        self.assertEqual(response.status_code, 401)

    def test_goal_update_from_other_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.put(reverse('needs:goal_detail', kwargs={'pk': 3}), {
            'name': 'newNameForGoal1',
            'description': 'newDescriptionForGoal1',
            'endDate': self.today,
            'need': self.need2.id,
        }, format='json')

        self.assertEqual(response.status_code, 403)

    # ==============================================test_goal_delete=======================================

    def test_goal_delete(self):
        count = Goal.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.delete(
            reverse('needs:goal_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 204)

        count = Goal.objects.all().count()
        self.assertEqual(count, 2)

    def test_goal_delete_no_loged_user(self):
        count = Goal.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        response = client.delete(
            reverse('needs:goal_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 401)

        count = Goal.objects.all().count()
        self.assertEqual(count, 3)

    def test_goal_delete_from_other_user(self):
        count = Goal.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.delete(
            reverse('needs:goal_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 403)

        count = Goal.objects.all().count()
        self.assertEqual(count, 3)


class StepViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'root1', 'email1@exemple.com', 'root')
        self.user2 = User.objects.create_user(
            'root2', 'email2@exemple.com', 'root')

        self.need1 = Need.objects.create(
            name='need1', description='need1 description', user=self.user1)
        self.need2 = Need.objects.create(
            name='need2', description='need2 description', user=self.user2)

        self.goal1 = Goal.objects.create(name="goal1", need=self.need1)
        self.goal2 = Goal.objects.create(name="goal2", need=self.need2)
        self.goal3 = Goal.objects.create(name="goal1", need=self.need1)

        self.step1 = Step.objects.create(name='step1', description='step1Description',
                                         completed=False, goal=self.goal1)
        self.step2 = Step.objects.create(name='step2', description='step2Description',
                                         completed=False, goal=self.goal1)
        self.step3 = Step.objects.create(name='step3', description='step3Description',
                                         completed=False, goal=self.goal2)

    # ==============================================test_step_create=======================================

    def test_step_creation(self):
        count = Step.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.post(reverse('needs:step_list'), {
            'name': 'newStep',
            'description': 'newStepDescription',
            'completed': True,
            'goal': self.goal2.id,
        }, format='json')

        self.assertEqual(response.status_code, 201)
        count = Step.objects.all().count()
        self.assertEqual(count, 4)

    def test_step_creation_no_loged_user(self):
        count = Step.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()

        response = client.post(reverse('needs:step_list'), {
            'name': 'newStep',
            'description': 'newStepDescription',
            'completed': True,
            'goal': self.goal2.id,
        }, format='json')

        self.assertEqual(response.status_code, 401)
        count = Step.objects.all().count()
        self.assertEqual(count, 3)

    # ==============================================test_step_list=======================================

    def test_step_list(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get(reverse('needs:step_list'))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 2)

    def test_step_list_no_loged_user(self):
        client = APIClient()

        response = client.get(reverse('needs:step_list'))
        self.assertEqual(response.status_code, 401)

    def test_step_list_by_goal(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get(
            reverse('needs:step_list_by_goal', kwargs={'goal': 1}))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 2)

        self.step3 = Step.objects.create(name='step4', description='step4Description',
                                         completed=False, goal=self.goal3)

        response = client.get(
            reverse('needs:step_list_by_goal', kwargs={'goal': 1}))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 2)

    # ==============================================test_step_retrieve======================================

    def test_step_retrieve(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get(reverse('needs:step_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['name'], 'step1')
        self.assertEqual(data['description'], 'step1Description')
        self.assertEqual(data['completed'], False)
        self.assertEqual(data['goal'], self.goal1.id)

    def test_step_retrieve_no_loged_user(self):
        client = APIClient()
        response = client.get(reverse('needs:step_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 401)

    def test_step_retrieve_from_other_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get(reverse('needs:step_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 403)

    def test_step_retrieve_with_percentage_completed_no_deliveries(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get(reverse('needs:step_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['name'], 'step1')
        self.assertEqual(data['description'], 'step1Description')
        self.assertEqual(data['completed'], False)
        self.assertEqual(data['goal'], self.goal1.id)
        self.assertEqual(data['percentageCompleted'], '0%')

    def test_step_retrieve_with_percentage_completed_one_deliverie_completed_100(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        Delivery.objects.create(name="",description="", step=self.step1, completed=True)

        response = client.get(reverse('needs:step_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['name'], 'step1')
        self.assertEqual(data['description'], 'step1Description')
        self.assertEqual(data['completed'], False)
        self.assertEqual(data['goal'], self.goal1.id)
        self.assertEqual(data['percentageCompleted'], '100.0%')

    def test_step_retrieve_with_percentage_completed_one_of_two_deliverie_completed_50(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        Delivery.objects.create(name="",description="", step=self.step1, completed=True)
        Delivery.objects.create(name="aiai",description="ds", step=self.step1)

        response = client.get(reverse('needs:step_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['name'], 'step1')
        self.assertEqual(data['description'], 'step1Description')
        self.assertEqual(data['completed'], False)
        self.assertEqual(data['goal'], self.goal1.id)
        self.assertEqual(data['percentageCompleted'], '50.0%')

    # ==============================================test_step_update=======================================

    def test_step_update(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.put(reverse('needs:step_detail', kwargs={'pk': 1}), {
            'name': 'step1Updated',
            'description': 'step1DescriptionUpdated',
            'completed': True,
            'goal': self.goal2.id,
        }, format='json')

        self.assertEqual(response.status_code, 200)
        step = Step.objects.get(id=1)
        self.assertEqual(step.name, 'step1Updated')
        self.assertEqual(step.description, 'step1DescriptionUpdated')
        self.assertIs(step.completed, True)
        self.assertEqual(step.goal, self.goal2)

    def test_step_update_no_loged_user(self):
        client = APIClient()

        response = client.put(reverse('needs:step_detail', kwargs={'pk': 1}), {
            'name': 'step1Updated',
            'description': 'step1DescriptionUpdated',
            'completed': True,
            'goal': self.goal2.id,
        }, format='json')

        self.assertEqual(response.status_code, 401)

    def test_step_update_from_other_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.put(reverse('needs:step_detail', kwargs={'pk': 3}), {
            'name': 'step1Updated',
            'description': 'step1DescriptionUpdated',
            'completed': True,
            'goal': self.goal2.id,
        }, format='json')

        self.assertEqual(response.status_code, 403)

    # ==============================================test_step_delete=======================================

    def test_step_delete(self):
        count = Step.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.delete(
            reverse('needs:step_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 204)

        count = Step.objects.all().count()
        self.assertEqual(count, 2)

    def test_step_delete_no_loged_user(self):
        count = Step.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()

        response = client.delete(
            reverse('needs:step_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 401)

        count = Step.objects.all().count()
        self.assertEqual(count, 3)

    def test_step_delete_from_other_user(self):
        count = Step.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.delete(
            reverse('needs:step_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 403)

        count = Step.objects.all().count()
        self.assertEqual(count, 3)


class IterationViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'root1', 'email1@exemple.com', 'root')
        self.user2 = User.objects.create_user(
            'root2', 'email2@exemple.com', 'root')

        self.need1 = Need.objects.create(
            name='need1', description='need1 description', user=self.user1)
        self.need2 = Need.objects.create(
            name='need2', description='need2 description', user=self.user2)

        self.goal1 = Goal.objects.create(name="goal1", need=self.need1)
        self.goal2 = Goal.objects.create(name="goal2", need=self.need2)
        self.goal3 = Goal.objects.create(name="goal1", need=self.need1)

        self.step1 = Step.objects.create(name='step1', description='step1Description',
                                         completed=False, goal=self.goal1)
        self.step2 = Step.objects.create(name='step2', description='step2Description',
                                         completed=False, goal=self.goal1)
        self.step3 = Step.objects.create(name='step3', description='step3Description',
                                         completed=False, goal=self.goal1)

        self.iteration1 = Iteration.objects.create(number=1, completed=True,
                                                   date=datetime.date.today(), owner=self.user1)
        self.iteration2 = Iteration.objects.create(number=2, completed=False,
                                                   date=datetime.date.today(), owner=self.user1)
        self.iteration3 = Iteration.objects.create(number=1, completed=True,
                                                   date=datetime.date.today(), owner=self.user2)

    # ==============================================test_iteration_create===================================

    def test_iteration_creation(self):
        count = Iteration.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.post(reverse('needs:iteration_list'), {
            'number': 2,
            'completed': True,
            'date': datetime.date.today(),
        }, format='json')

        self.assertEqual(response.status_code, 201)
        count = Iteration.objects.all().count()
        self.assertEqual(count, 4)

        iteration = Iteration.objects.get(pk=4)
        self.assertEqual(iteration.number, 2)
        self.assertEqual(iteration.completed, True)
        self.assertEqual(iteration.date, datetime.date.today())
        self.assertEqual(iteration.owner, self.user1)

    def test_iteration_creation_no_loged_user(self):
        count = Iteration.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()

        response = client.post(reverse('needs:iteration_list'), {
            'number': 2,
            'completed': True,
            'date': datetime.date.today(),
            'goal': self.goal2.id,
        }, format='json')

        self.assertEqual(response.status_code, 401)
        count = Iteration.objects.all().count()
        self.assertEqual(count, 3)

    # ==============================================test_iteration_list===================================

    def test_iteration_list(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(reverse('needs:iteration_list'))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 2)

    def test_iteration_list_no_loged_user(self):
        client = APIClient()
        response = client.get(reverse('needs:iteration_list'))
        self.assertEqual(response.status_code, 401)

    # ==============================================test_iteration_update===================================

    def test_iteration_update(self):
        count = Iteration.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.put(reverse('needs:iteration_detail', kwargs={'pk': 1}), {
            'number': 2,
            'completed': True,
            'date': datetime.date.today(),
            'owner': self.user1.id,
        }, format='json')
        self.assertEqual(response.status_code, 200)
        count = Iteration.objects.all().count()
        self.assertEqual(count, 3)

        iteration = Iteration.objects.get(id=1)
        self.assertEqual(iteration.number, 2)
        self.assertIs(iteration.completed, True)
        self.assertEqual(iteration.date, datetime.date.today())
        self.assertEqual(iteration.owner, self.user1)

    def test_iteration_update_no_loged_user(self):
        count = Iteration.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()

        response = client.put(reverse('needs:iteration_detail', kwargs={'pk': 1}), {
            'number': 2,
            'completed': True,
            'date': datetime.date.today(),
            'owner': self.user1.id,
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_iteration_update_from_other_user(self):

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.put(reverse('needs:iteration_detail', kwargs={'pk': 3}), {
            'number': 2,
            'completed': True,
            'date': datetime.date.today(),
            'owner': self.user2.id,
        }, format='json')
        self.assertEqual(response.status_code, 403)

    # ==============================================test_iteration_retrieve===================================

    def test_iteration_retrieve(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get(
            reverse('needs:iteration_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['number'], self.iteration1.number)
        self.assertEqual(data['completed'], self.iteration1.completed)
        self.assertEqual(data['date'], str(self.iteration1.date))

    def test_iteration_retrieve_no_loged_user(self):
        client = APIClient()

        response = client.get(
            reverse('needs:iteration_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 401)

    def test_iteration_retrieve_from_other_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get(
            reverse('needs:iteration_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 403)

    def test_active_iteration_retrieve(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get(reverse('needs:active_iteration'))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['number'], self.iteration2.number)
        self.assertEqual(data['completed'], self.iteration2.completed)
        self.assertEqual(data['date'], str(self.iteration2.date))

    def test_active_iteration_retrieve_no_active_iteration(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)

        response = client.get(reverse('needs:active_iteration'))
        self.assertEqual(response.status_code, 404)

    # ==============================================test_iteration_delete===================================

    def test_iteration_delete(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        count = Iteration.objects.all().count()
        self.assertEqual(count, 3)

        response = client.delete(
            reverse('needs:iteration_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 204)

        count = Iteration.objects.all().count()
        self.assertEqual(count, 2)

    def test_iteration_delete_no_loged_user(self):
        client = APIClient()

        count = Iteration.objects.all().count()
        self.assertEqual(count, 3)

        response = client.delete(
            reverse('needs:iteration_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 401)

        count = Iteration.objects.all().count()
        self.assertEqual(count, 3)

    def test_iteration_delete_from_other_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        count = Iteration.objects.all().count()
        self.assertEqual(count, 3)

        response = client.delete(
            reverse('needs:iteration_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 403)

        count = Iteration.objects.all().count()
        self.assertEqual(count, 3)


class DeliveryViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'root1', 'email1@exemple.com', 'root')
        self.user2 = User.objects.create_user(
            'root2', 'email2@exemple.com', 'root')

        self.need1 = Need.objects.create(
            name='need1', description='need1 description', user=self.user1)
        self.need2 = Need.objects.create(
            name='need2', description='need2 description', user=self.user2)

        self.goal1 = Goal.objects.create(name="goal1", need=self.need1)
        self.goal2 = Goal.objects.create(name="goal2", need=self.need2)

        self.step1 = Step.objects.create(name='step1', description='step1Description',
                                         completed=False, goal=self.goal1)
        self.step2 = Step.objects.create(name='step2', description='step2Description',
                                         completed=False, goal=self.goal2)
        self.step3 = Step.objects.create(name='step3', description='step3Description',
                                         completed=False, goal=self.goal1)

        self.iteration1 = Iteration.objects.create(number=1, completed=False,
                                                   date=datetime.date.today(), owner=self.user1)
        self.iteration2 = Iteration.objects.create(number=2, completed=False,
                                                   date=datetime.date.today(), owner=self.user1)
        self.iteration3 = Iteration.objects.create(number=1, completed=True,
                                                   date=datetime.date.today(), owner=self.user2)

        self.delivery1 = Delivery.objects.create(name='delivery1', description='delivery1Description',
                                                 step=self.step1, iteration=self.iteration1, completed=False)
        self.delivery2 = Delivery.objects.create(name='delivery2', description='delivery2Description',
                                                 step=self.step1, iteration=self.iteration1, completed=False)
        self.delivery3 = Delivery.objects.create(name='delivery3', description='delivery1Description',
                                                 step=self.step2, iteration=self.iteration3, completed=False)

    # ==============================================test_delivery_create===================================

    def test_delivery_creation(self):
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.post(reverse('needs:delivery_list'), {
            'name': 'newIteration',
            'description': 'newIterationDescription',
            'step': self.step2.id,
            'iteration': self.iteration1.id,
            'completed': True,
        }, format='json')

        self.assertEqual(response.status_code, 201)
        count = Delivery.objects.all().count()
        self.assertEqual(count, 4)

    def test_delivery_creation_with_name_length_60(self):
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.post(reverse('needs:delivery_list'), {
            'name': '012345678901234567890123456789012345678901234567890123456789',
            'description': 'newIterationDescription',
            'step': self.step2.id,
            'iteration': self.iteration1.id,
            'completed': True,
        }, format='json')

        self.assertEqual(response.status_code, 201)
        count = Delivery.objects.all().count()
        self.assertEqual(count, 4)

    def test_delivery_creation_no_loged_user(self):
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()

        response = client.post(reverse('needs:delivery_list'), {
            'name': 'newIteration',
            'description': 'newIterationDescription',
            'step': self.step2.id,
            'iteration': self.iteration1.id,
            'completed': True,
        }, format='json')

        self.assertEqual(response.status_code, 401)
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)

    # ==============================================test_delivery_list===================================

    def test_delivery_list(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(reverse('needs:delivery_list'))

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

    def test_delivery_list_no_loged_user(self):
        client = APIClient()
        response = client.get(reverse('needs:delivery_list'))

        self.assertEqual(response.status_code, 401)

    def test_delivery_list_by_step(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(
            reverse('needs:delivery_list_by_step', kwargs={'step': 1}))

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

        Delivery.objects.create(name='delivery3', description='delivery1Description',
                                step=self.step3, iteration=self.iteration3, completed=False)

        response = client.get(
            reverse('needs:delivery_list_by_step', kwargs={'step': 1}))

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

        Delivery.objects.create(name='delivery3', description='delivery1Description',
                                step=self.step1, iteration=self.iteration3, completed=False)

        response = client.get(
            reverse('needs:delivery_list_by_step', kwargs={'step': 1}))

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 3)

    def test_delivery_list_by_goal(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(
            reverse('needs:delivery_list_by_goal', kwargs={'goal': 1}))

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

        Delivery.objects.create(name='delivery3', description='delivery1Description',
                                step=self.step2, iteration=self.iteration3, completed=False)

        response = client.get(
            reverse('needs:delivery_list_by_goal', kwargs={'goal': 1}))

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

        Delivery.objects.create(name='delivery3', description='delivery1Description',
                                step=self.step3, iteration=self.iteration3, completed=False)

        response = client.get(
            reverse('needs:delivery_list_by_goal', kwargs={'goal': 1}))

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 3)

    def test_delivery_list_by_iteration(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.get(
            reverse('needs:delivery_list_by_iteration', kwargs={'iteration': 1}))

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

        Delivery.objects.create(name='delivery3', description='delivery1Description',
                                step=self.step3, iteration=self.iteration2, completed=False)

        response = client.get(
            reverse('needs:delivery_list_by_iteration', kwargs={'iteration': 1}))

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

        Delivery.objects.create(name='delivery3', description='delivery1Description',
                                step=self.step1, iteration=self.iteration1, completed=False)

        response = client.get(
            reverse('needs:delivery_list_by_iteration', kwargs={'iteration': 1}))

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 3)

    # ==============================================test_delivery_retrieve===================================

    def test_delivery_retrieve(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get(
            reverse('needs:delivery_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['name'], 'delivery1')
        self.assertEqual(data['description'], 'delivery1Description')
        self.assertEqual(data['step'], self.step1.id)
        self.assertEqual(data['iteration'], self.iteration1.id)
        self.assertEqual(data['completed'], False)

    def test_delivery_retrieve_no_loged_user(self):
        client = APIClient()

        response = client.get(
            reverse('needs:delivery_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 401)

    def test_delivery_retrieve_from_other_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.get(
            reverse('needs:delivery_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 403)

    # ==============================================test_delivery_update===================================

    def test_delivery_update(self):
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.put(reverse('needs:delivery_detail', kwargs={'pk': 1}), {
            'name': 'Iteration1Updated',
            'description': 'Iteration1DescriptionUpdated',
            'step': self.step2.id,
            'iteration': self.iteration1.id,
            'completed': True,
        }, format='json')

        self.assertEqual(response.status_code, 200)
        count = Iteration.objects.all().count()
        self.assertEqual(count, 3)

        delivery = Delivery.objects.get(id=1)
        self.assertEqual(delivery.name, 'Iteration1Updated')
        self.assertEqual(delivery.description, 'Iteration1DescriptionUpdated')
        self.assertEqual(delivery.step, self.step2)
        self.assertEqual(delivery.iteration, self.iteration1)
        self.assertIs(delivery.completed, True)

    def test_delivery_update_no_loged_user(self):
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()

        response = client.put(reverse('needs:delivery_detail', kwargs={'pk': 1}), {
            'name': 'Iteration1Updated',
            'description': 'Iteration1DescriptionUpdated',
            'step': self.step2.id,
            'iteration': self.iteration1.id,
            'completed': True,
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_delivery_update_from_other_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.put(reverse('needs:delivery_detail', kwargs={'pk': 3}), {
            'name': 'Iteration1Updated',
            'description': 'Iteration1DescriptionUpdated',
            'step': self.step2.id,
            'iteration': self.iteration1.id,
            'completed': True,
        }, format='json')
        self.assertEqual(response.status_code, 403)

    # ==============================================test_delivery_delete===================================

    def test_delivery_delete(self):
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.delete(
            reverse('needs:delivery_detail', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 204)
        count = Delivery.objects.all().count()
        self.assertEqual(count, 2)

    def test_delivery_delete_no_loged_user(self):
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()

        response = client.delete(
            reverse('needs:delivery_detail', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 401)
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)

    def test_delivery_delete_from_other_user(self):
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.delete(
            reverse('needs:delivery_detail', kwargs={'pk': 3}))

        self.assertEqual(response.status_code, 403)
        count = Delivery.objects.all().count()
        self.assertEqual(count, 3)


class UserViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'root1', 'email1@exemple.com', 'root')
        self.user2 = User.objects.create_user(
            'root2', 'email2@exemple.com', 'root')

    def test_user_creation(self):
        count = User.objects.all().count()
        self.assertEqual(count, 2)

        client = APIClient()

        response = client.post('/rest-auth/registration/',
                               {
                                   'username': 'newNeed',
                                   'email': 'aiaiai@gmail.com',
                                   'password1': 'newneedDescription',
                                   'password2': 'newneedDescription',
                               }, format='json')

        count = User.objects.all().count()
        self.assertEqual(count, 3)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['key'], data['key'])
        # self.assertEqual(response.status_code , 201)

        # count = Need.objects.all().count()
        # self.assertEqual(count, 4)

        # need = Need.objects.get(id=4)
        # self.assertEqual(need.description, 'newneedDescription')
        # self.assertEqual(need.name, 'newNeed')
        # self.assertEqual(need.user, self.user1

    def test_user_login(self):

        client = APIClient()

        response = client.post('/rest-auth/registration/',
                               {
                                   'username': 'newNeed',
                                   'email': 'aiaiai@gmail.com',
                                   'password1': 'newneedDescription',
                                   'password2': 'newneedDescription',
                               }, format='json')

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        key = data['key']

        response = client.post('/rest-auth/login/',
                               {
                                   'username': 'newNeed',
                                   'password': 'newneedDescription',
                               }, format='json')

        count = User.objects.all().count()
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(key, data['key'])

    def test_new_user_wizard(self):
        client = APIClient()

        response = client.post('/rest-auth/registration/',
                               {
                                   'username': 'newNeed',
                                   'email': 'aiaiai@gmail.com',
                                   'password1': 'newneedDescription',
                                   'password2': 'newneedDescription',
                               }, format='json')

        self.assertEqual(response.status_code, 201)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        key = data['key']

        client2 = APIClient()
        client2.credentials(HTTP_AUTHORIZATION='Token ' + key)

        response = client2.get(reverse('needs:need_list'), format='json')
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 0)

        response = client2.post(reverse('needs:wizard'), format='json')
        self.assertEqual(response.status_code, 200)

        response = client2.get(reverse('needs:need_list'), format='json')
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 5)


    def test_new_user_wizard_iteration(self):
        client = APIClient()

        response = client.post('/rest-auth/registration/',
                               {
                                   'username': 'newNeed',
                                   'email': 'aiaiai@gmail.com',
                                   'password1': 'newneedDescription',
                                   'password2': 'newneedDescription',
                               }, format='json')

        self.assertEqual(response.status_code, 201)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        key = data['key']

        client2 = APIClient()
        client2.credentials(HTTP_AUTHORIZATION='Token ' + key)

        response = client2.get(reverse('needs:iteration_list'), format='json')
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 0)

        response = client2.post(reverse('needs:wizard'), format='json')
        self.assertEqual(response.status_code, 200)

        response = client2.get(reverse('needs:iteration_list'), format='json')
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 1)


    def test_tutorial_goal_with_steps_and_deliveries_create(self):
        client = APIClient()

        response = client.post('/rest-auth/registration/',
                               {
                                   'username': 'newNeed',
                                   'email': 'aiaiai@gmail.com',
                                   'password1': 'newneedDescription',
                                   'password2': 'newneedDescription',
                               }, format='json')

        self.assertEqual(response.status_code, 201)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        key = data['key']

        client2 = APIClient()
        client2.credentials(HTTP_AUTHORIZATION='Token ' + key)

        response = client2.post(reverse('needs:wizard'), format='json')
        self.assertEqual(response.status_code, 200)

        response = client2.get(reverse('needs:goal_list'), format='json')
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 0)

        response = client2.post(reverse('needs:tutorial_setup'), format='json')
        self.assertEqual(response.status_code, 200)

        response = client2.get(reverse('needs:goal_list'), format='json')
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 1)

        response = client2.get(reverse('needs:step_list'), format='json')
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 4)

        response = client2.get(reverse('needs:delivery_list'), format='json')
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 1)


