# Pac-Man

Tento projekt je jednoduchá 2D implementace klasické hry Pac-Man vytvořená v Pythonu s využitím knihovny Pygame.

## O hře

Cílem hry je, aby hráč v roli Pac-Mana snědl všechny mince v bludišti a zároveň se vyhnul duchům.

## Herní mechaniky

- **Mince**: Sbíráním mincí hráč získává body.
- **Power-upy**: Po snědení speciální mince (`*`) získá Pac-Man dočasnou schopnost jíst duchy.
- **Teleporty**: Na okrajích herního plánu jsou teleporty, které Pac-Mana přenesou na druhou stranu.
- **Životy**: Pac-Man začíná se 3 životy. Pokud ho chytí duch, ztratí život.
- **Skóre**: Hráč získává body za sbírání mincí a pojídání duchů.

## Postavy

### Pac-Man
Hráčem ovládaná postava.

### Duchové
V bludišti se nachází čtyři duchové s různým chováním:
- **Aggro Ghost**: Pronásleduje Pac-Mana.
- **Dumb Ghost**: Pohybuje se náhodně.
- **Pattern Ghost (2x)**: Pohybují se po předem definované trase.

## Instalace a spuštění

1.  Naklonujte si repozitář.
2.  Ujistěte se, že máte nainstalovaný Python a knihovny `pygame` a `pytest`.
    ```bash
    pip install pygame pytest
    ```
3.  Spusťte hru příkazem:
    ```bash
    python -m src.Game
    ```

## Ovládání

- **Pohyb**: Šipkami (nahoru, dolů, doleva, doprava).
- **Restart**: Po skončení hry stiskněte mezerník pro restart.
- **Výběr motivu**: V menu si můžete pomocí myši vybrat barevný motiv bludiště.

## Testování

Pro spuštění testů použijte příkaz:
```bash
python -m pytest tests
```
