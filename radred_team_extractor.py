import struct
import pandas as pd
import streamlit as st

abilities_df = pd.read_csv("species_abilities.csv")


def _load_lines(filename):
    with open(filename, "r", encoding="utf-8", errors="replace") as f:
        return [line.strip() for line in f]


SPECIES_NAMES = _load_lines("Species.txt")
MOVES_LIST = _load_lines("Moves.txt")
ITEMS_LIST = _load_lines("Items.txt")


def _species_name(sid):
    if 1 <= sid <= len(SPECIES_NAMES):
        return SPECIES_NAMES[sid - 1]
    return None


def _move_name(mid):
    if 1 <= mid <= len(MOVES_LIST):
        return MOVES_LIST[mid - 1]
    return None


def _item_name(iid):
    if iid == 0 or iid > len(ITEMS_LIST):
        return None
    return ITEMS_LIST[iid - 1]


def _ability_name(species, ab_type):
    row = abilities_df[abilities_df["Species"] == species]
    if row.empty:
        return "Unknown"
    col = {"1": "Primary Ability", "2": "Secondary Ability", "h": "Hidden Ability"}.get(
        ab_type, "Primary Ability"
    )
    val = row[col].values[0]
    return val if pd.notna(val) else "Unknown"


# GBA save file layout (FRLG / Radical Red 4.1)
SECTION_SIZE = 0x1000
NUM_SECTIONS = 14
SECTION_ID_OFFSET = 0x0FF4
SIGNATURE_OFFSET = 0x0FF8
SAVE_INDEX_OFFSET = 0x0FFC
EXPECTED_SIGNATURE = 0x08012025
SAVE_FILE_SIZE = 128 * 1024

PARTY_COUNT_OFFSET = 0x0034
PARTY_DATA_OFFSET = 0x0038
PARTY_ENTRY_SIZE = 100
BOX_ENTRY_SIZE = 80
MAX_PARTY = 6
NUM_BOXES = 14
SLOTS_PER_BOX = 30

# Sections 5-13 hold PC storage; each section contributes 3968 (0xF80) bytes of payload.
SECTION_DATA_SIZE = 0x0F80
PC_BOX_DATA_OFFSET = 4  # u32 currentBox sits before the pokemon array

NATURES = {
    0: "Hardy", 1: "Lonely", 2: "Brave", 3: "Adamant", 4: "Naughty",
    5: "Bold", 6: "Docile", 7: "Relaxed", 8: "Impish", 9: "Lax",
    10: "Timid", 11: "Hasty", 12: "Serious", 13: "Jolly", 14: "Naive",
    15: "Modest", 16: "Mild", 17: "Quiet", 18: "Bashful", 19: "Rash",
    20: "Calm", 21: "Gentle", 22: "Sassy", 23: "Careful", 24: "Quirky",
}

GBA_CHARMAP = {
    0x00: " ", 0x01: "À", 0x02: "Á", 0x03: "Â", 0x04: "Ç", 0x05: "È",
    0x06: "É", 0x07: "Ê", 0x08: "Ë", 0x09: "Ì", 0x0A: " ", 0x0B: "Î",
    0x0C: "Ï", 0x0D: "Ò", 0x0E: "Ó", 0x0F: "Ô", 0x10: "Œ", 0x11: "Ù",
    0x12: "Ú", 0x13: "Û", 0x14: "Ñ", 0x15: "ß", 0x16: "à", 0x17: "á",
    0x18: " ", 0x19: "ç", 0x1A: "é", 0x1B: "ê", 0x1C: "ë", 0x1D: "ì",
    0x1E: "í", 0x1F: " ", 0x20: "ï", 0x21: "ò", 0x22: "ó", 0x23: "ô",
    0x24: "œ", 0x25: "ù", 0x26: "ú", 0x27: "û", 0x28: "", 0x29: "ñ",
    0x2A: "ª", 0x2B: "º", 0x2C: "ᵉʳ", 0x2D: "&", 0x2E: "+", 0x2F: "=",
    0x30: ";", 0x31: "¿", 0x32: "¡", 0x33: "Pk", 0x34: "Mn", 0x35: "Po",
    0x36: "ké", 0x37: "Í", 0x38: "%", 0x39: "(", 0x3A: ")", 0x3B: "▾",
    0x3C: "▸", 0x3D: "▹", 0x3E: "♀", 0x3F: "♂",
    0x40: " ", 0x41: " ", 0x42: " ", 0x43: " ", 0x44: " ", 0x45: " ",
    0x46: " ", 0x47: " ", 0x48: " ", 0x49: " ", 0x4A: " ", 0x4B: " ",
    0x4C: " ", 0x4D: " ", 0x4E: " ", 0x4F: " ",
    0x50: " ", 0x51: " ", 0x52: " ", 0x53: " ", 0x54: " ", 0x55: " ",
    0x56: " ", 0x57: " ", 0x58: " ", 0x59: " ", 0x5A: " ", 0x5B: " ",
    0x5C: " ", 0x5D: " ", 0x5E: " ", 0x5F: " ",
    0x60: " ", 0x61: " ", 0x62: " ", 0x63: " ", 0x64: " ", 0x65: " ",
    0x66: " ", 0x67: " ", 0x68: " ", 0x69: " ", 0x6A: " ", 0x6B: " ",
    0x6C: " ", 0x6D: " ", 0x6E: " ", 0x6F: " ",
    0x70: " ", 0x71: " ", 0x72: " ", 0x73: " ", 0x74: " ", 0x75: " ",
    0x76: " ", 0x77: " ", 0x78: " ", 0x79: " ", 0x7A: " ", 0x7B: " ",
    0x7C: " ", 0x7D: " ", 0x7E: " ", 0x7F: " ",
    0x80: "0", 0x81: "1", 0x82: "2", 0x83: "3", 0x84: "4", 0x85: "5",
    0x86: "6", 0x87: "7", 0x88: "8", 0x89: "9", 0x8A: "!", 0x8B: "?",
    0x8C: ".", 0x8D: "-", 0x8E: "·", 0x8F: "…",
    0x90: "\u201c", 0x91: "\u201d", 0x92: " ", 0x93: " ", 0x94: "♂",
    0x95: "♀", 0x96: "$", 0x97: ",", 0x98: " ", 0x99: "÷",
    0x9A: " ", 0x9B: " ", 0x9C: " ", 0x9D: " ", 0x9E: " ", 0x9F: " ",
    0xA0: "ʳᵉ", 0xA1: "0", 0xA2: "1", 0xA3: "2", 0xA4: "3", 0xA5: "4",
    0xA6: "5", 0xA7: "6", 0xA8: "7", 0xA9: "8", 0xAA: "9", 0xAB: "!",
    0xAC: "?", 0xAD: ".", 0xAE: "-", 0xAF: "･",
    0xB0: "‥", 0xB1: "\u201c", 0xB2: "\u201d", 0xB3: "\u2018", 0xB4: "'",
    0xB5: "♂", 0xB6: "♀", 0xB7: "$", 0xB8: ",", 0xB9: "×", 0xBA: "/",
    0xBB: "A", 0xBC: "B", 0xBD: "C", 0xBE: "D", 0xBF: "E",
    0xC0: "F", 0xC1: "G", 0xC2: "H", 0xC3: "I", 0xC4: "J", 0xC5: "K",
    0xC6: "L", 0xC7: "M", 0xC8: "N", 0xC9: "O", 0xCA: "P", 0xCB: "Q",
    0xCC: "R", 0xCD: "S", 0xCE: "T", 0xCF: "U",
    0xD0: "V", 0xD1: "W", 0xD2: "X", 0xD3: "Y", 0xD4: "Z", 0xD5: "a",
    0xD6: "b", 0xD7: "c", 0xD8: "d", 0xD9: "e", 0xDA: "f", 0xDB: "g",
    0xDC: "h", 0xDD: "i", 0xDE: "j", 0xDF: "k",
    0xE0: "l", 0xE1: "m", 0xE2: "n", 0xE3: "o", 0xE4: "p", 0xE5: "q",
    0xE6: "r", 0xE7: "s", 0xE8: "t", 0xE9: "u", 0xEA: "v", 0xEB: "w",
    0xEC: "x", 0xED: "y", 0xEE: "z", 0xEF: "►",
    0xF0: ":", 0xF1: "Ä", 0xF2: "Ö", 0xF3: "Ü", 0xF4: "ä", 0xF5: "ö",
    0xF6: "ü", 0xF7: " ", 0xF8: " ", 0xF9: " ", 0xFA: " ", 0xFB: " ",
    0xFC: " ", 0xFD: " ", 0xFE: " ", 0xFF: "",
}


def _decode_name(raw):
    out = ""
    for b in raw:
        if b == 0xFF:
            break
        out += GBA_CHARMAP.get(b, "")
    return out.rstrip()


def _get_sections(sav_data):
    """Return {section_id: section_bytes} from the newest of the two save blocks."""
    if len(sav_data) != SAVE_FILE_SIZE:
        raise ValueError(
            f"Invalid save file size: {len(sav_data):,} bytes (expected {SAVE_FILE_SIZE:,})"
        )

    blocks = [{}, {}]
    block_indices = [0, 0]

    for blk in range(2):
        for sec in range(NUM_SECTIONS):
            off = (blk * NUM_SECTIONS + sec) * SECTION_SIZE
            data = sav_data[off : off + SECTION_SIZE]
            sid = struct.unpack_from("<H", data, SECTION_ID_OFFSET)[0]
            sig = struct.unpack_from("<I", data, SIGNATURE_OFFSET)[0]
            si = struct.unpack_from("<I", data, SAVE_INDEX_OFFSET)[0]
            if sig == EXPECTED_SIGNATURE and sid < NUM_SECTIONS:
                blocks[blk][sid] = data
                block_indices[blk] = max(block_indices[blk], si)

    latest = 0 if block_indices[0] >= block_indices[1] else 1
    if not blocks[latest]:
        raise ValueError("No valid save data found")
    return blocks[latest]


def _parse_pokemon(buf, is_party):
    """Parse one Pokemon from raw bytes (100 for party, 80 for box). Returns dict or None.

    Radical Red v4.1 stores substructure data unencrypted in fixed GAEM order,
    so the byte offsets match the canonical layout without needing XOR decryption
    or personality-based reordering.
    """
    if len(buf) < BOX_ENTRY_SIZE:
        return None

    pid = struct.unpack_from("<I", buf, 0)[0]
    if pid == 0:
        return None

    species_id = struct.unpack_from("<H", buf, 32)[0]
    if species_id == 0 or species_id > len(SPECIES_NAMES):
        return None

    species = _species_name(species_id)
    if not species:
        return None

    nickname = _decode_name(buf[8:18])
    item = _item_name(struct.unpack_from("<H", buf, 34)[0])

    move_ids = struct.unpack_from("<4H", buf, 44)
    moves = [_move_name(m) for m in move_ids if m != 0]
    moves = [m for m in moves if m is not None]

    ev_hp, ev_atk, ev_def, ev_spd, ev_spa, ev_spd2 = struct.unpack_from("6B", buf, 56)

    iv_word = struct.unpack_from("<I", buf, 72)[0]
    iv_hp = iv_word & 0x1F
    iv_atk = (iv_word >> 5) & 0x1F
    iv_def = (iv_word >> 10) & 0x1F
    iv_spd = (iv_word >> 15) & 0x1F
    iv_spa = (iv_word >> 20) & 0x1F
    iv_spd2 = (iv_word >> 25) & 0x1F
    is_egg = bool((iv_word >> 30) & 1)
    ability_bit = (iv_word >> 31) & 1

    ab_type = "h" if ability_bit else ("1" if pid % 2 == 0 else "2")
    ability = _ability_name(species, ab_type)
    nature = NATURES[pid % 25]

    level = None
    if is_party and len(buf) >= 85:
        level = buf[84]

    return {
        "species": species,
        "nickname": nickname,
        "level": level,
        "item": item,
        "ability": ability,
        "nature": nature,
        "moves": moves,
        "evs": {
            "HP": ev_hp, "Atk": ev_atk, "Def": ev_def,
            "SpA": ev_spa, "SpD": ev_spd2, "Spe": ev_spd,
        },
        "ivs": {
            "HP": iv_hp, "Atk": iv_atk, "Def": iv_def,
            "SpA": iv_spa, "SpD": iv_spd2, "Spe": iv_spd,
        },
        "is_egg": is_egg,
    }


def extract_pokemon(sav_data):
    """Return (party_list, boxes_dict) from raw save bytes.

    boxes_dict maps box number (1-14) -> list of pokemon dicts.
    """
    sections = _get_sections(sav_data)

    # ── Party (section 1) ────────────────────────────────────
    party = []
    sec1 = sections.get(1)
    if sec1:
        count = min(
            struct.unpack_from("<I", sec1, PARTY_COUNT_OFFSET)[0], MAX_PARTY
        )
        for i in range(count):
            off = PARTY_DATA_OFFSET + i * PARTY_ENTRY_SIZE
            pkmn = _parse_pokemon(sec1[off : off + PARTY_ENTRY_SIZE], is_party=True)
            if pkmn and not pkmn["is_egg"]:
                party.append(pkmn)

    # ── PC boxes (sections 5-13 concatenated) ────────────────
    pc_blob = bytearray()
    for sid in range(5, 14):
        sec = sections.get(sid)
        if sec:
            pc_blob.extend(sec[:SECTION_DATA_SIZE])

    boxes = {}
    if len(pc_blob) > PC_BOX_DATA_OFFSET:
        for bx in range(NUM_BOXES):
            mons = []
            for slot in range(SLOTS_PER_BOX):
                off = PC_BOX_DATA_OFFSET + (bx * SLOTS_PER_BOX + slot) * BOX_ENTRY_SIZE
                if off + BOX_ENTRY_SIZE > len(pc_blob):
                    break
                pkmn = _parse_pokemon(
                    pc_blob[off : off + BOX_ENTRY_SIZE], is_party=False
                )
                if pkmn and not pkmn["is_egg"]:
                    mons.append(pkmn)
            if mons:
                boxes[bx + 1] = mons

    return party, boxes


def to_showdown(p):
    """Format a single Pokemon in Showdown paste syntax."""
    nick = p["nickname"].strip()
    sp = p["species"]
    header = f"{nick} ({sp})" if nick and nick != sp else sp
    if p["item"]:
        header += f" @ {p['item']}"

    lines = [header, f"Ability: {p['ability']}"]

    if p["level"] is not None:
        lines.append(f"Level: {p['level']}")

    ev_parts = [f"{v} {k}" for k, v in p["evs"].items() if v > 0]
    if ev_parts:
        lines.append("EVs: " + " / ".join(ev_parts))

    lines.append(f"{p['nature']} Nature")

    iv_parts = [f"{v} {k}" for k, v in p["ivs"].items() if v != 31]
    if iv_parts:
        lines.append("IVs: " + " / ".join(iv_parts))

    lines.extend(f"- {m}" for m in p["moves"])
    return "\n".join(lines)


# ── Streamlit UI ─────────────────────────────────────────────

st.set_page_config(
    page_title="Radical Red Team Exporter", page_icon="radredicon.ico"
)
st.title("Radical Red v4.1 Team Exporter")
st.caption(
    "Upload a save file to export every Pokemon (party + PC boxes) in Showdown format."
)

# type=None accepts ALL file types — critical for iOS where .sav has no
# registered MIME type and the system file picker would otherwise hide it.
uploaded = st.file_uploader(
    "Upload your save file",
    type=None,
    help=(
        "iOS users: if your .sav file isn't visible in the picker, "
        "try renaming it to .bin or use the Files app to browse for it."
    ),
)

if uploaded:
    raw = uploaded.read()
    if len(raw) != SAVE_FILE_SIZE:
        st.error(
            f"Invalid file — expected exactly 128 KB ({SAVE_FILE_SIZE:,} bytes), "
            f"got {len(raw):,} bytes."
        )
    else:
        try:
            party, boxes = extract_pokemon(raw)
            if not party and not boxes:
                st.warning("No Pokemon found in this save file.")
            else:
                full_text = ""

                if party:
                    st.subheader(f"Party ({len(party)})")
                    txt = "\n\n".join(to_showdown(p) for p in party)
                    full_text += txt
                    st.code(txt, language="")

                for bnum, mons in sorted(boxes.items()):
                    st.subheader(f"Box {bnum} ({len(mons)})")
                    txt = "\n\n".join(to_showdown(p) for p in mons)
                    if full_text:
                        full_text += "\n\n"
                    full_text += txt
                    st.code(txt, language="")

                total = len(party) + sum(len(m) for m in boxes.values())
                st.download_button(
                    "Download All (.txt)",
                    full_text.strip(),
                    file_name="showdown_export.txt",
                    mime="text/plain",
                )
                st.toast(f"Loaded {total} Pokemon!", icon="\u2705")
        except Exception as e:
            st.error(f"Error reading save file: {e}")
