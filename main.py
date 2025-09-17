# basically wrap around this https://stackoverflow.com/a/27194892
import pathlib
from dataclasses import fields

from catppuccin import PALETTE
from catppuccin.models import RGB
from catppuccin.models import Flavor as Flavour

ctpLatte = PALETTE.latte
ctpFrappe = PALETTE.frappe
ctpMacchiato = PALETTE.macchiato
ctpMocha = PALETTE.mocha
flavours = [ctpLatte, ctpFrappe, ctpMacchiato, ctpMocha]


def convertRGBto565(colour: RGB) -> int:
    """Converts from RGB to 565 format

    Converts a Catppuccin Colour (in RGB format) to 565 format.

    Parameters
    ----------
    colour : RGB
        Catppuccin Color.RGB

    Returns
    -------
    int
        Integer representation of input colour in 565 format

    Examples
    --------
    FIXME: Add docs.

    """
    r, g, b = colour.r, colour.g, colour.b
    red = r >> 3
    green = g >> 2
    blue = b >> 3
    result = (red << (5 + 6)) | (green << 5) | blue
    return result


def writeAllColoursToFile(filename: pathlib.Path) -> None:
    """Writes all the colours from all the flavours to a file
    This is useful for if you want multiple flavours at the same time

    Parameters
    ----------
    filename : pathlib.Path
        file to write to

    Examples
    --------
    FIXME: Add docs.
    """
    filename.parent.mkdir(exist_ok=True, parents=True)
    with open(filename, "w", encoding="utf-8") as file:
        for flavour in flavours:
            flavourComment = flavour.name
            file.write(f"/*{flavourComment:=^47}*/\n")
            for field in fields(flavour.colors):
                color = getattr(flavour.colors, field.name)
                identiferColor = f"{flavour.identifier.upper()}_{field.name.upper()}"
                file.write(
                    f"#define CATPPUCCIN_{identiferColor:<25}{hex(convertRGBto565(color.rgb))}\n"
                )
            file.write("\n")
    file.close()


def writeColoursToFile(filename: pathlib.Path, flavour: Flavour) -> None:
    """Writes colours into a file per flavour
    Writes the flavours into a file named `{flavour}_Catppuccin_TFT_eSPI.h` -
    good for if you want to reuse colour names and only use one flavour at a
    time (otherwise you will have redefinition's)

    Parameters
    ----------
    filename : pathlib.Path
        File to write flavours to
    flavour : Flavour
        Flavour to write out

    Examples
    --------
    FIXME: Add docs.
    """
    filename.parent.mkdir(exist_ok=True, parents=True)
    with open(filename, "w", encoding="utf-8") as file:
        flavourComment = flavour.name
        file.write(f"/*{flavourComment:=^32}*/\n")
        for field in fields(flavour.colors):
            fieldNameIdentifier = f"{field.name.upper()}"
            color = getattr(flavour.colors, field.name)
            file.write(
                f"#define CATPPUCCIN_{fieldNameIdentifier:<10}{hex(convertRGBto565(color.rgb))}\n"
            )
    file.close()


def main() -> None:
    writeAllColoursToFile(pathlib.Path("include/") / "AllFlavoursCatppuccin_TFT_eSPI.h")
    for flavour in flavours:
        filename = f"{flavour.identifier.capitalize()}Catppuccin_TFT_eSPI.h"
        pathToFile = pathlib.Path("include/") / filename
        writeColoursToFile(pathToFile, flavour)


if __name__ == "__main__":
    main()
