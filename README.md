## Macro 
원시적이고 담백한 매크로ps

## Guide: proseka
### Requirements
- NoxPlayer 기준, 1280x720 화면 필요
- Python package
  - `pygetwindow`
  - `pyautogui`
  - `pynput`
  - `system_hotkey`
- 인게임
  - 힐덱 필요 (다 채울 필요는 x)
  - 'Hitorinbo Envy' 악곡 필요

### Steps
- "솔로 라이브" > "악곡 선택" 메뉴에 위치
- "Hitorinbo Envy", 난이도 Easy로 설정후 매크로 시작

### Making executable
- `pyinstaller main.py`
- `macro.config` 제대로 위치시키는 거 잊지 말기 

### Config
- `PLAYER_WINDOWNAME` 윈도우 이름
- `PROSEKA_REPEAT` 반복 횟수 기본값
- `PROSEKA_REFILL_RATE` 충전 빈도 기본값

