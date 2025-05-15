# THALYSRUN0
## coregame
### install-dev

git clone <me>

```bash
python -m venv coregame-venv
source coregame-venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python coregame/test.py
```

actual ERROR:
... coregame/test.py", line 46, in update
self.ball.rigidbody.velocity.reflect(player1_hit.normal)  
ValueError: Normal must not be of length zero.  
-> collider.check_collision::Hit(normal) is pygame.Vector2(0, 0) 