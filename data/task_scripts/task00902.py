# Copyright (c) Facebook, Inc. and its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Template task in which two balls should touch each other."""
import numpy as np
import phyre.creator as creator_lib


@creator_lib.define_task_template(
    bar_y=np.linspace(0.05, 0.3, 5),
    ball1_x=np.linspace(0.05, 0.85, 8),
    ball2_x=np.linspace(0.85, 0.95, 3),
    ball1_r=np.linspace(0.05, 0.25, 5),
    ball2_r=np.linspace(0.05, 0.25, 5),
    ramp_angle=np.linspace(135.0, 160.0, 6),
    search_params=dict(
        max_search_tasks=100),
        # required_flags=['BALL:TRIVIAL']),
    version='2',
)
def build_task(C, ball1_x, ball2_x, ball1_r, ball2_r, bar_y, ramp_angle):

    # Generate static bar.
    scene_width = C.scene.width
    scene_height = C.scene.height
    bar = C.add('static bar', scale=1.0) \
           .set_bottom(bar_y * scene_height) \
           .set_left(0.0)

    # Task definition is symmetric.
    if ball2_x <= ball1_x:
        raise creator_lib.SkipTemplateParams

    # Add ramp.
    ramp_l = C.add('static bar', scale=1.0) \
            .set_angle(ramp_angle) \
            .set_left(0.0) \
            .set_bottom(bar.top)

    # Add two balls.
    ball1 = C.add( # left ball
        'dynamic ball',
        scale=ball1_r,
        center_x=ball1_x * C.scene.width)
    ball2 = C.add( # right ball
        'dynamic ball',
        scale=ball2_r,
        center_x=ball2_x * C.scene.width,
        bottom=bar.top)
    # if (ball2.left - ball1.right) < max(ball1_r, ball2_r) * C.scene.width:
    #     raise creator_lib.SkipTemplateParams
    if ball1.center_x - 0.05 >= ramp_l.right:
        raise creator_lib.SkipTemplateParams
    if ball1.bottom <= bar.top:
        raise creator_lib.SkipTemplateParams
    if ball1.left <= 0:
        raise creator_lib.SkipTemplateParams
    if ball2.right >= C.scene.width - 1:
        raise creator_lib.SkipTemplateParams

    # Create assignment:
    C.update_task(
        body1=ball1,
        body2=ball2,
        relationships=[C.SpatialRelationship.TOUCHING])
    C.set_meta(C.SolutionTier.BALL)
