import sys
sys.path.append('/home/llin/coporate_training/universal')
import tools
import message


def generate_alert_to_grade(receiver):
    msg = '''
Hi team,

This is an test email. Please notice that:
- The code is still largely a trial, please let Luke know if you see any bug.
- The Unix exam can be taken care by Luke now. Shu, could you review the unix exam since you will eventually be the grader for that.


This is the daily summary of new exam that we need to grade.....Thank you!

%s
        ''' % str(tools.alert_ungraded_exam())

    msg = message.CreateMessage(
        'luke.lin@nycdatascience.com',
        receiver,
        'test',
        msg
    )
    return msg

graders = ['luke.lin@nycdatascience.com', 'zeyu.zhang@nycdatascience.com', 'shu.yan@nycdatascience.com']

if __name__ == '__main__':
    tools.add_requirement()
    tools.update_exam_from_enrollment()
    for receiver in graders:
        message.SendMessage(message.service, 'me', generate_alert_to_grade(receiver))
