# r: compas_fab>=1.0.2
"""
Publishes messages to a ROS topic

COMPAS FAB v1.0.2
"""

import time

import Grasshopper
from compas_ghpython import create_id
from roslibpy import Topic
from scriptcontext import sticky as st

from compas_fab.backends.ros.messages import ROSmsg
from compas_fab.ghpython.components import message
from compas_fab.ghpython.components import warning


class ROSTopicPublish(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self, ros_client, topic_name: str, topic_type: str, msg):
        if not topic_name:
            warning(ghenv.Component, "Please specify the name of the topic")
            return
        if not topic_type:
            warning(ghenv.Component, "Please specify the type of the topic")
            return

        key = create_id(ghenv.Component, "topic")  # noqa: F821

        topic = st.get(key, None)

        if ros_client and ros_client.is_connected:
            if not topic or topic.ros != ros_client:
                topic = Topic(ros_client, topic_name, topic_type, reconnect_on_close=False)
                topic.advertise()
                time.sleep(0.2)

                st[key] = topic

        self.is_advertised = topic and topic.is_advertised

        if msg:
            msg = ROSmsg.parse(msg, topic_type)
            topic.publish(msg.msg)
            message(ghenv.Component, "Message published")
        else:
            if self.is_advertised:
                message(ghenv.Component, "Topic advertised")

        return (topic, self.is_advertised)
