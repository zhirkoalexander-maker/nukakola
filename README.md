# Base Defense - Tower Builder Game

A strategic tower defense game built with Python and Pygame where you defend your base by building structures, hiring units, and defeating waves of enemies.

## Features

### 🏰 Building System
- 10 different block types with varying health and costs
- Intuitive grid-based building mechanics
- Breakable blocks for resource management
- Destructible blocks generate loot and currency

### 🎖️ Unit System
- Hire 3 types of NPCs to assist in defense:
  - **Archer**: Long-range attacker, fast attack speed
  - **Warrior**: Close-range tank, moderate damage
  - **Mage**: Medium-range caster, balanced stats
- Units have limited 10-second lifespan
- Units automatically pursue and attack enemies
- Low damage per unit to require strategic gameplay

### ⚔️ Weapon System
- 6 unique weapons with different stats:
  - Sword: Balanced melee weapon
  - Axe: Heavy damage, slow
  - Spear: Long range, fast
  - Sniper: Extreme range, very high damage
  - Hammer: Devastating AoE damage
  - Laser: Medium damage with beam effect

### 🎮 Game Modes
1. **Classic Mode** - Balanced difficulty with moderate enemy waves
2. **Hard Mode** - Increased enemy count and faster spawn rates
3. **Survival Mode** - Endless waves with rapid escalation

### 🎨 UI/UX
- Full readable text labels throughout interface
- Organized UI panels in corners without overlapping
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
- **X** - Sword
- **C** - Axe
- **V** - Spear
- **Z** - Sniper
- **F** - Hammer
- **L** - Laser

### Game Flow
- **P** - Pause/Resume game
- **ESC** - Return to main menu
- **SPACE** - Restart after game over

## Installation

### Requirements
- Python 3.8+
- Pygame

### Setup
```bash
# Clone the repository
git clone https://github.com/zhirkoalexander-maker/nukakola.git
cd nukakola

# Create virtual environment (optional)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install pygame

# Run the game
python building_game.py
```

## Game Strategy

### Early Game
- Focus on building defensive structures around your base
- Collect loot and accumulate currency
- Start hiring units as soon as you can afford them

### Mid Game
- Expand your defenses with stronger block types (stone, iron, crystal)
- Maintain multiple unit helpers for better coverage
- Switch to weapon mode when enemies breach defenses

### Late Game
- Balance between building reinforcements and hiring units
- Use expensive, high-tier blocks for critical areas
- Manage your economy to maintain steady unit recruitment

## Block Types

| Block | Health | Cost | Special |
|-------|--------|------|---------|
| Grass | 30 | 30 | Starting material |
| Wood | 40 | 40 | Basic structure |
| Brick | 60 | 70 | Medium durability |
| Sand | 25 | 25 | Weak filler |
| Stone | 80 | 80 | Strong structure |
| Iron | 150 | 150 | Very durable |
| Crystal | 120 | 120 | Specialized |
| Obsidian | 200 | 250 | Excellent defense |
| Diamond | 300 | 400 | Ultimate defense |
| Titanium | 180 | 200 | Expert material |

## NPC Unit Specs

| Unit | Cost | Health | Damage | Range |
|------|------|--------|--------|-------|
| Archer | 120 | 25 | 4 | 250px |
| Warrior | 150 | 35 | 3 | 80px |
| Mage | 140 | 20 | 5 | 200px |

## Enemy Types

- **Zombie** - Basic enemy
- **Fast** - Quick but fragile
- **Heavy** - Slow but durable
- **Ranged** - Attacks from distance
- **Healer** - Can heal other enemies (later waves)

## Performance

- Optimized for 60 FPS gameplay
- Efficient collision detection
- Particle system with cleanup
- Minimal memory footprint

## Development

Built with:
- **Python 3** - Core language
- **Pygame** - Graphics and game engine
- **Math module** - Physics and calculations

## Future Enhancements

- [ ] Sound effects and background music
- [ ] Animated sprites
- [ ] Improved enemy AI
- [ ] Tower defense elements
- [ ] Leaderboard system
- [ ] Additional game modes
- [ ] Customization options

## License

This project is open source and available under the MIT License.

## Author

**zhirkoalexander-maker** - Game Developer

## Support

If you find bugs or have feature requests, feel free to open an issue on GitHub!

---

**Last Updated:** February 22, 2026
