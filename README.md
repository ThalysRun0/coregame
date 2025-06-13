# coregame
## install-dev

git clone \<me\>

```bash
cd coregame
python<version> -m venv coregame-venv
source coregame-venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python coregame/zpong.py
```
## report
-2025.05.15  
actual ERROR:
... coregame/test.py", line 46, in update  
self.ball.rigidbody.velocity.reflect(player1_hit.normal)  
ValueError: Normal must not be of length zero.  
-> collider.check_collision::Hit(normal) is pygame.Vector2(0, 0)  

-2025.05.16  
ValueError: Normal must not be of length zero. (solved)  
but introduced an artefact rotating around paddle  
nice effect but not intended  

### TODO
- **pending** UnIncr  
make it in a seperate class in assets  
also make it functional  
the objective is to disable some scene object while decrement is pending  

- **pending** multi-ball  
adding multi ball generation by pressing a keyboard key  
pending work about convex collision  

- **pending** snake game  
first version with lot of work to do  

- **done** generic way to check for collision  
... coregame/test.py", line 40, in update  
self.check_collision() # TODO: need refinement  
all Gameobject collides with eachother in the scene

## pending-doc
### install not dev

git clone \<me\>

```bash
mkdir yourgame
cd yourgame
python -m venv yourgame-venv
source yourgame-venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python coregame/test.py
```

New file `yourgame.py`  
```file
from coregame.game import Game
from coregame.scene import Scene
from coregame.gameobject import Gameobject
```
Add a new Scene class `class YourScene(Scene):`  
Add some sub-new Gameobject class `class YourFunObject(Gameobject)`  
Add a new class `class YourGame(Game):`  
Your may want to separate all this class in different files  
