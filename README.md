# Base Defense - Tower Builder Game

A strategic tower defense game built with Python and Pygame where you defend your base by building structures, hiring units, and defeating waves of enemies.

**🌐 Website:** https://zhirkoalexander-maker.github.io/nukakola/

## ⚡ Quick Start

```bash
# 1. Install Python 3.8+
# 2. Install Pygame
pip install pygame

# 3. Clone and run
git clone https://github.com/zhirkoalexander-maker/nukakola.git
cd nukakola
python building_game.py
```

## Features

### 🏰 Building System
- 10 different block types with textures and varying health/costs
- Intuitive grid-based building mechanics
- Breakable blocks for resource management
- Destructible blocks generate loot and currency

### 🎖️ Unit System
- Hire 3 types of NPCs to assist in defense:
  - **Archer**: $120 - Long-range attacker, fast attack speed
  - **Warrior**: $150 - Close-range tank, moderate damage
  - **Mage**: $140 - Medium-range caster, balanced stats
- Units have limited 10-second lifespan
- Units automatically pursue and attack enemies
- Low damage per unit to require strategic gameplay

### ⚔️ Weapon System
- 6 unique weapons with different stats:
  - **Sword**: 30 damage, balanced melee
  - **Axe**: 35 damage, heavy hits
  - **Spear**: 25 damage, long reach
  - **Sniper**: 80 damage, extreme range
  - **Hammer**: 50 damage, area effect
  - **Laser**: 45 damage, beam attack

### 🎮 Game Modes
1. **Classic Mode** - 3 enemies/wave, +2 scaling - Balanced difficulty
2. **Hard Mode** - 5 enemies/wave, +3 scaling - Challenging
3. **Survival Mode** - 4 enemies/wave, +4 scaling - Endless waves

### 🎨 UI/UX
- Full readable text labels throughout interface
- Organized UI panels in corners without overlapping
- Settings menu with volume control
- "How to Play" tutorial screen
- Real-time status displays:
  - Wave counter and enemy count
  - Score and earnings
  - Health and resource management
  - Active unit count
  - Weapon statistics
  - Active buff indicators

### 📊 Game Mechanics
- Wave-based enemy progression
- Dynamic difficulty scaling
- Monetary rewards for defeating enemies
- Power-ups: Speed boost, shield, mega strike
- Projectile animations with visual effects
- Particle effects for destruction and impacts

## Controls

### Movement & Interaction
- **WASD** - Move character
- **Left Mouse Click** - Build blocks, break blocks, or attack
- **1/2/3** - Switch between Build, Break, and Weapon modes

### Weapon Selection

## Installation

### System Requirements
- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 1GB minimum (4GB recommended)
- **Display**: 1280x720 minimum (1920x1080 recommended)

### Installation Steps

#### 1. Install Python
- Download from [python.org](https://www.python.org)
- **Important**: During installation, check "Add Python to PATH"
- Verify: `python --version`

#### 2. Clone Repository
```bash
git clone https://github.com/zhirkoalexander-maker/nukakola.git
cd nukakola
```

#### 3. Install Pygame
```bash
pip install pygame
```

#### 4. Run Game
```bash
python building_game.py
```

### Troubleshooting
| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: pygame` | Run `pip install pygame` |
| `Python not found` | Restart terminal after Python installation |
| `Command not found` | Use full path: `/usr/bin/python3 building_game.py` |
| Game runs slow | Close other apps or update graphics drivers |

## Game Controls

### Movement
- **W** - Move up
- **A** - Move left
- **S** - Move down
- **D** - Move right

### Building & Modes
- **1** - Build mode
- **2** - Break mode
- **3** - Weapon mode

### Weapons
- **X** - Sword
- **C** - Axe
- **V** - Spear
- **Z** - Sniper
- **F** - Hammer
- **L** - Laser

### Game Controls
- **P** - Pause/Resume
- **ESC** - Return to menu

## Game Strategy

### Early Game (Waves 1-5)
- Build defensive walls around base core
- Collect initial loot and currency
- Hire your first helper units

### Mid Game (Waves 6-15)
- Upgrade to stronger blocks (stone, iron)
- Maintain 2-3 active helper units
- Manage economy carefully
- Switch to weapon mode during peak waves

### Late Game (Waves 15+)
- Use diamond and titanium for critical areas
- Keep units rotating (10-second lifespan)
- Focus on base survival
- In Survival mode: maintain constant unit hiring

## Block Materials

| Block | Health | Cost | Best Use |
|-------|--------|------|----------|
| 🌳 Grass | 30 | 30 | Temporary walls |
| 🌲 Wood | 40 | 40 | Basic structures |
| 🧱 Brick | 60 | 70 | Medium defense |
| 🏜️ Sand | 25 | 25 | Filler blocks |
| 🪨 Stone | 80 | 80 | Primary defense |
| ⚙️ Iron | 150 | 150 | Heavy defense |
| 💎 Crystal | 120 | 120 | Specialized |
| ⬛ Obsidian | 200 | 250 | Strong walls |
| 💍 Diamond | 300 | 400 | Ultimate defense |
| 🔷 Titanium | 180 | 200 | Expert defense |

## NPC Units

| Unit | Cost | Health | Damage | Range | Speed |
|------|------|--------|--------|-------|-------|
| 🏹 Archer | $120 | 25 | 4 | 250px | 1.8 |
| ⚔️ Warrior | $150 | 35 | 3 | 80px | 2.0 |
| 🧙 Mage | $140 | 20 | 5 | 200px | 1.5 |

All units last 10 seconds and auto-attack enemies within range.

## Enemy Types

- **🧟 Zombie** (30 HP) - Basic enemy, 1.5 speed
- **🏃 Fast** (15 HP) - Quick attacker, 2.8 speed  
- **🛡️ Heavy** (60 HP) - Tank unit, 0.8 speed
- **🏹 Ranged** (25 HP) - Distance attacker, 1.2 speed
- **💚 Healer** (20 HP) - Heals other enemies, 0.9 speed

## Project Structure

```
nukakola/
├── building_game.py          # Main game (1673 lines)
├── README.md                 # This file
├── COMPLETION_SUMMARY.md     # Project stats
├── textures/                 # Game textures
│   ├── Bricks002_*.jpg      # Brick textures
│   └── Grass001_*.jpg       # Grass textures
├── docs/                     # GitHub Pages website
│   ├── index.html           # Game documentation
│   └── README.md            # Website info
└── .git/                     # Git repository
```

## Performance

- **FPS**: Optimized for 60 FPS
- **Resolution**: 1280x720 (scalable)
- **Memory**: ~50MB typical usage
- **CPU**: Low usage (even on older systems)

## About

**Base Defense** is a strategic tower defense game that emphasizes:
- Resource management
- Tactical positioning
- Dynamic difficulty
- Strategic unit hiring
- Real-time combat

Perfect for players who enjoy:
- Strategy games
- Tower defense mechanics
- Resource management
- Tower building challenges

## License

This project is created for educational and entertainment purposes.

## Author

[GitHub: zhirkoalexander-maker](https://github.com/zhirkoalexander-maker)

## Resources

- 🌐 [Play Online Documentation](https://zhirkoalexander-maker.github.io/nukakola/)
- 📦 [GitHub Repository](https://github.com/zhirkoalexander-maker/nukakola)
- 🐍 [Python.org](https://www.python.org)
- 🎮 [Pygame Library](https://pygame.org)

---

**Enjoy the game! 🎮⚔️🏰**


## License

This project is open source and available under the MIT License.

## Author

**zhirkoalexander-maker** - Game Developer

## Support

If you find bugs or have feature requests, feel free to open an issue on GitHub!

---

**Last Updated:** February 22, 2026
