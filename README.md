# Chess ♟️

A fully-featured, rule-compliant chess game implementation in Python with a graphical Pygame interface. This project provides a complete chess engine with support for all standard moves, special cases (castling, en passant, promotion), and proper game-state management.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Game Controls](#game-controls)
- [Architecture](#architecture)
- [Module Documentation](#module-documentation)
  - [main.py](#mainpy)
  - [pieces.py](#piecespy)
  - [player.py](#playerpy)
  - [constants.py](#constantspy)
- [Testing](#testing)
- [License](#license)

## Features

### Core Gameplay
- **Full Chess Rule Implementation**: All standard chess moves and rules are correctly implemented
- **Piece-Specific Movement Logic**: Each piece type (Pawn, Rook, Knight, Bishop, Queen, King) has its own movement rules
- **Check & Checkmate Detection**: Automatic detection and handling of check, checkmate, and stalemate conditions
- **Move Validation**: Legal move calculation with check-filtering to prevent self-check situations

### Special Moves
- **Castling**: King-side and queen-side castling with full legality validation
- **En Passant**: Proper en passant pawn capture detection and execution
- **Pawn Promotion**: Automatic promotion detection when pawns reach the back rank, with selection of promotion pieces (Queen, Rook, Knight, Bishop)

### User Interface
- **Graphical Game Board**: 800×800 pixel display with maple wood board aesthetic
- **Visual Feedback**: 
  - Check indicator (red blur effect on the king)
  - Green circles showing legal moves for selected pieces
  - Piece selection highlighting
- **Turn Indicator**: Window title displays current player and move count
- **Move Logging**: Terminal output for game state changes and move history

### Architecture & Testing
- **Modular Design**: Clean separation of concerns across player management, piece logic, and UI
- **Configurable Player Setup**: Support for standard, king-only, and empty board setups (useful for testing)
- **Move History Tracking**: Algebraic notation logging of all moves
- **Test Infrastructure**: Pytest configuration for unit testing

## Project Structure

```
chess/
├── main.py                 # Game loop and Pygame interface
├── pieces.py               # Chess piece classes and movement logic
├── player.py               # Player state management and piece collection
├── constants.py            # Display configuration constants
├── pytest.ini              # Pytest configuration
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT license
├── assets/
│   ├── boards/            # Board textures
│   ├── check_indicators/  # Check state indicators
│   └── piece_sets/
│       └── cburnett/      # Chess piece images in SVG format
└── tests/                 # Test suite (pytest)
```

## Requirements

- **Python**: 3.10+ (uses Python 3.10+ type hints: `type Position = tuple[int, int]`)
- **Pygame-ce**: 2.0+
- **Pytest**: 7.0+ (for running tests)

## Installation

### Clone the Repository

```bash
git clone https://github.com/Orbit-Phrase-Sea/chess.git
cd chess
```

### Install Dependencies

```bash
pip install pygame-ce pytest
```

## Usage

### Start the Game

```bash
python main.py
```

The game will launch in a window. White moves first.

### Run Tests

```bash
python -m pytest
```

## Game Controls

| Action | Key/Input |
|--------|-----------|
| **Select Piece** | Left-click on a piece |
| **Move Piece** | Left-click on a highlighted legal square |
| **Promote Pawn** | Press `1` (Queen), `2` (Rook), `3` (Knight), or `4` (Bishop) when prompted |
| **Quit Game** | Press `ESC` or close the window |

### Game Flow

1. **Piece Selection**: Click a piece to select it; green dots appear showing legal moves
2. **Movement**: Click a legal square to move the piece
3. **Special Moves**: 
   - Castling and en passant occur automatically when valid
   - Pawn promotion is prompted with keyboard input
4. **Game End**: The game detects checkmate or stalemate automatically and displays the result

## Architecture

### Design Patterns

- **Object-Oriented Design**: Each piece type is a class inheriting from a base `Piece` class
- **Separation of Concerns**: 
  - `pieces.py` handles piece logic
  - `player.py` manages player state
  - `main.py` orchestrates the game loop and UI
- **Type Safety**: Uses Python 3.10+ type hints for clarity and IDE support

### Game State Management

- **Turn Management**: Alternates between white ('w') and black ('b') players
- **Move Validation**: Each piece calculates its legal moves; moves are filtered to exclude moves that leave the player in check
- **Board Representation**: 8×8 coordinate system (0–7 for both x and y)
- **En Passant Tracking**: `Player.en_passant_capturable` tracks the last pawn that moved two squares

## Module Documentation

### main.py

**Purpose**: Entry point and game loop. Manages the Pygame interface, event handling, and game state.

**Key Components**:
- **Display Setup**: Initializes Pygame window with title and FPS capping
- **Asset Loading**: Loads board image, check indicator, and all piece images
- **Game Loop**: Continuous loop that:
  - Processes mouse clicks to select and move pieces
  - Detects check, checkmate, and stalemate
  - Renders the board and pieces
  - Handles pawn promotion prompts
- **Event Handling**: 
  - Left-click for piece selection/movement
  - Keyboard input (1–4) for promotion selection
  - ESC key or window close to quit
- **Move Counter**: Tracks full moves (half-moves divided by 2)

**Key Variables**:
- `color_to_move`: Current player's color ('w' or 'b')
- `game_over`: Boolean flag for game completion
- `promotion_in_progress`: Flag indicating pawn promotion in progress

### pieces.py

**Purpose**: Defines all chess piece classes and movement logic.

**Special Features**:
- **King**: `castles_legality_check()` validates castling conditions (king/rook not moved, clear path, not in check)
- **Pawn**: Handles forward moves, captures, en passant, and promotion detection
- **All Pieces**: Check filtering ensures no move leaves the player in check

### player.py

**Purpose**: Manages a single player's state, pieces, and piece interactions.

**Key Components**:
- `Player.__init__(color, piece_setup)`: Initializes player with optional piece configurations
  - `'default'`: Standard chess starting position (king, queen, rooks, bishops, knights, pawns)
  - `'king'`: Only king (useful for testing)
  - `'empty'`: No pieces (useful for custom board setups)
- **Piece Management**: Maintains `active_piece_list` of all player's pieces

**Key Methods**:
- `check_for_piece_selection(position)`: Handles piece selection/deselection logic
- `move_selected_piece(opponent, position)`: Moves the selected piece; validates and applies special rules
  - Detects and removes captured pieces
  - Handles en passant captures
  - Handles castling (moves the rook automatically)
  - Sets up en passant capturable state
- `promote(promotion_id)`: Replaces pawn with chosen piece (1=Queen, 2=Rook, 3=Knight, 4=Bishop)
- `is_to_promote()`: Detects pawns reaching the back rank
- `get_king()` / `set_king()`: King management
- `get_piece_objects()` / `get_piece_img_filenames()`: Access piece data
- `set_en_passant_capturable()` / `get_en_passant_capturable()`: En passant state tracking

**Special Features**:
- **Move History**: Stores algebraic notation of all moves in `move_history`
- **En Passant Tracking**: Automatically detects and marks pawns vulnerable to en passant after two-square moves
- **Castling Automation**: Automatically moves the rook when the king castles

### constants.py

**Purpose**: Centralized display configuration.

**Display Class** (frozen dataclass):
```python
WIDTH: int = 800      # Game window width in pixels
HEIGHT: int = 800     # Game window height in pixels
FPS: int = 20         # Frame rate cap
```

These constants are used throughout `main.py` for:
- Window initialization
- Board and piece positioning
- Mouse click coordinate mapping to board squares

---

## Testing

The project includes a **Pytest configuration** (`pytest.ini`) for automated testing

### Running Tests

```bash
# Run all tests
python -m pytest
```

### Testing Strategy

The modular architecture supports testing at multiple levels:
- **Unit Tests**: Test individual piece movement rules
- **Integration Tests**: Test player state management and move execution
- **Game State Tests**: Test check, checkmate, and stalemate detection using the `'king'` and `'empty'` piece setups

**Example Test Setup**:
```python
from player import Player

# Create empty boards for testing
white = Player('w', piece_setup='empty')
black = Player('b', piece_setup='empty')

# Add specific pieces for testing isolated scenarios
```

---

## Implementation Highlights

### Move Validation Pipeline

1. **Piece-Specific Moves**: Each piece calculates all pseudo-legal moves
2. **Ally Piece Filtering**: Removes moves to squares occupied by friendly pieces
3. **Capture Handling**: Marks moves to opponent pieces as valid captures
4. **Check Filtering**: `_filter_for_checks()` removes moves that leave/put the king in check
5. **Return Legal Moves**: Returns final list of truly legal moves

### Special Case Handling

| Case | Implementation |
|------|-----------------|
| **Castling** | `King.castles_legality_check()` validates: king/rook not moved, clear path, king not in/through check |
| **En Passant** | Pawn tracks `opponent.en_passant_capturable`; diagonal move to empty square captures the pawn |
| **Pawn Promotion** | `Player.is_to_promote()` detects rank 7/0 pawns; `Player.promote()` replaces pawn with selected piece |
| **Check/Checkmate** | `King.check_for_checks()` tests if king is under attack; checkmate = check + no legal moves |

---

## License

MIT License – See [LICENSE](LICENSE) file for details.

Copyright © 2026 Orbit-Phrase-Sea

---

## Contributing

Contributions are welcome! The codebase is well-structured for extension:
- Add new board themes in `assets/boards/`
- Implement AI players by extending `Player`
- Add time controls by modifying `main.py`
- Expand test coverage with additional scenarios

---

## Future Enhancement Ideas

- **AI Opponent**: Minimax or neural network-based chess engine
- **Move Undo/Redo**: Store and revert game states
- **PGN Export/Import**: Save and load games in standard notation
- **Network Play**: Multiplayer over sockets or WebSockets
- **Opening Book**: Integrate recognized opening variations
- **Endgame Tablebases**: Optimal play in reduced piece scenarios

