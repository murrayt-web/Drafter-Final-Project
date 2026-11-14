from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("Your Drafter Website")
set_website_framed(False)


from drafter import *
from dataclasses import dataclass

Free_Throw_Distance = 15
Three_Point_Distance = 22
@dataclass
class Shot:
    distance: int
    angle: int
    velocity: int
    made: bool
    
@dataclass

class State:
    player_name: str
    shot_type: str
    shots: list[Shot]
    made_shots: int
    
def check_make(distance: int, angle: int, velocity: int) -> bool:
    ''' Returns True if the angle and velocity are good enough '''
    if angle < 45 or angle > 55:
        return False
    if distance == Free_Throw_Distance:
        return velocity >= 24 and velocity <=26
    return velocity >=27 and velocity <= 29
@route
def index(state: State) -> Page:
    ''' home page where user enters their name'''
    return Page(state, [
        "Basketball Shot Calculator",
        "Welcome " + state.player_name,
        TextBox("name", state.player_name),
        Button("Save Name", save_name),
        Button("Take a Shot", shot_setup),
        Button("Shot History", shot_history),
        Button("Stats", stats)
    ])
@route

def save_name(state: State, name: str) -> Page:
    ''' saves players name'''
    state.player_name = name
    return index(state)



@route

def shot_setup(state: State) -> Page:
    '''  where user picks a shot type'''
    return Page(state, [
        "Shot type:",
        SelectBox("shot_type", ["Free Throw", "Three-Pointer"], state.shot_type),
        "Angle (degrees):",
        TextBox("angle", "50"),
        "Velocity (ft/s):",
        TextBox("velocity", "25"),
        Button("Shoot!", take_shot),
        Button("Home", index)
    ])

@route

def take_shot(state: State, shot_type: str, angle: int, velocity: int) -> Page:
    ''' takes shot, saves, shows if it went in'''
    state.shot_type = shot_type
    if shot_type == "Free Throw":
        distance = Free_Throw_Distance
    else:
        distance = Three_Point_Distance
    made = check_make(distance, angle, velocity)
    state.shots.append(Shot(distance, angle, velocity, made))
    if made:
        state.made_shots = state.made_shots + 1
        message = "Swish!"
    else:
        message = "Miss!"
    return Page(state, [
        message,
        Button("Shoot Again", shot_setup),
        Button("Home", index)
    ])
@route

def shot_history(state: State) -> Page:
    ''' shows every shot taken'''
    if len(state.shots) == 0:
        return Page(state, ["No shots yet.", Button("Home", index)])
    lines = []
    for shot in state.shots:
        if shot.made:
            result = "Make"
        else:
            result = "Miss"
        lines.append(str(shot.distance) + " ft, " + str(shot.angle) + " degrees, " + str(shot.velocity)
                     + " ft/s: " + result)
    return Page(state, ["Shot History"] + lines + [
        Button("Clear History", clear_history),
        Button("Home", index)
    ])

@route

def clear_history(state: State) -> Page:
    ''' deletes all shots'''
    state.shots = []
    state.made_shots = 0
    return shot_history(state)


@route

def stats(state: State) -> Page:
    ''' Shows made shots, total shots, and shooting percentage. '''
    total = len(state.shots)
    if total == 0:
        percent = 0
    else:
        percent = round(state.made_shots / total * 100)
    return Page(state, [
        "Made shots: " + str(state.made_shots) + " / " + str(total),
        "Shooting Percentage: " + str(percent) + "%",
        Button("Home", index)
    ])

assert_equal(check_make(15, 50, 25), True)
assert_equal(check_make(15, 30, 25), False)
assert_equal(check_make(22, 50, 28), True)


assert_equal(
    shot_setup(State("", "Free Throw", [], 0)),
    Page(State( "", "Free Throw", [], 0), [
        "Shot type:",
        SelectBox("shot_type", ["Free Throw", "Three-Pointer"], "Free Throw"),
        "Angle (degrees):",
        TextBox("angle", "50"),
        "Velocity (ft/s):",
        TextBox("velocity", "25"),
        Button("Shoot!", take_shot),
        Button("Home", index)
    ]))

assert_equal (take_shot(State("", "Free Throw", [], 0), "Free Throw", 50, 25),
              Page(State("", "Free Throw", [Shot(15, 50, 25, True)], 1), [
                  "Swish!",
                    Button("Shoot Again", shot_setup),
                    Button("Home", index)
                ]))

                   


assert_equal (take_shot(State("", "Free Throw", [], 0), "Three-Pointer", 50, 20),
                       Page(State("", "Three-Pointer", [Shot(22, 50, 20, False)], 0), [
                           "Miss!",
                           Button("Shoot Again", shot_setup),
                           Button("Home", index)
                        ]))
assert_equal(clear_history(State("", "Free Throw", [Shot(15, 50, 25, True)], 1)),
             Page(State("", "Free Throw", [], 0), ["No shots yet.", Button("Home", index)]))

                                 

assert_equal(shot_history(State("", "Free Throw", [], 0)),
             Page(State("", "Free Throw", [], 0), ["No shots yet.", Button("Home", index)]))
        
assert_equal(shot_history(State("", "Free Throw", [Shot(15, 50, 25, True)], 1)),
             Page(State("", "Free Throw", [Shot(15, 50, 25, True)], 1), [
                 "Shot History",
                 "15 ft, 50 degrees, 25 ft/s: Make",
                 Button("Clear History", clear_history),
                 Button("Home", index)
            ]))
assert_equal(
    stats(State("", "Free Throw", [Shot(15, 50, 25, True), Shot(22, 50, 20, False)], 1)),
    Page(State("", "Free Throw", [Shot(15, 50, 25, True), Shot(22, 50, 20, False)], 1), [
        "Made shots: 1 / 2",
        "Shooting Percentage: 50%",
        Button("Home", index)
    ]))


assert_equal(
    save_name(State("", "Free Throw", [], 0), "Ana"),
    Page(State("Ana", "Free Throw", [], 0), [
        "Basketball Shot Calculator",
        "Welcome Ana",
        TextBox("name", "Ana"),
        Button("Save Name", save_name),
        Button("Take a Shot", shot_setup),
        Button("Shot History", shot_history),
        Button("Stats", stats)
    ]))


assert_equal(
    index(State("Ana", "Free Throw", [], 0)),
    save_name(State("", "Free Throw", [], 0), "Ana"),
    Page(State("Ana", "Free Throw", [], 0), [
        "Basketball Shot Calculator",
        "Welcome Ana",
        TextBox("name", "Ana"),
        Button("Save Name", save_name),
        Button("Take a Shot", shot_setup),
        Button("Shot History", shot_history),
        Button("Stats", stats)
    ]))
        

start_server(State())
