import regex

from .parse import Parser
from .transformers import *


def add_defaults(parser: Parser):
    """
    Adds default handlers to the provided parser for various patterns such as episode codes, resolution,
    date formats, year ranges, etc. The handlers use regular expressions to match patterns and transformers
    to process the matched values.

    :param parser: The parser instance to which handlers will be added.
    """
    # Container
    parser.add_handler("container", regex.compile(r"\.?[\[(]?\b(MKV|AVI|MP4|WMV|MPG|MPEG)\b[\])]?", regex.IGNORECASE), lowercase)

    # Torrent extension
    parser.add_handler("torrent", regex.compile(r"\.torrent$"), boolean, {"remove": True})

    # Site before languages to get rid of domain name with country code.
    parser.add_handler("site", regex.compile(r"^(www?[\.,][\w-]+\.[\w-]+(?:\.[\w-]+)?)\s+-\s*", regex.IGNORECASE), options={"skipFromTitle": True, "remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("site", regex.compile(r"^((?:www?[\.,])?[\w-]+\.[\w-]+(?:\.[\w-]+)*?)\s+-\s*", regex.IGNORECASE), options={"skipIfAlreadyFound": False})
    parser.add_handler("site", regex.compile(r"\bwww.+rodeo\b", regex.IGNORECASE), lowercase, {"remove": True})

    # Resolution
    parser.add_handler("resolution", regex.compile(r"\[?\]?3840x\d{4}[\])?]?", regex.IGNORECASE), value("2160p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"\[?\]?1920x\d{3,4}[\])?]?", regex.IGNORECASE), value("1080p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"\[?\]?1280x\d{3}[\])?]?", regex.IGNORECASE), value("720p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"\[?\]?(\d{3,4}x\d{3,4})[\])?]?p?", regex.IGNORECASE), value("$1p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"(480|720|1080)0[pi]", regex.IGNORECASE), value("$1p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"(?:QHD|QuadHD|WQHD|2560(\d+)?x(\d+)?1440p?)", regex.IGNORECASE), value("1440p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"(?:Full HD|FHD|1920(\d+)?x(\d+)?1080p?)", regex.IGNORECASE), value("1080p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"(?:BD|HD|M)(2160p?|4k)", regex.IGNORECASE), value("2160p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"(?:BD|HD|M)1080p?", regex.IGNORECASE), value("1080p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"(?:BD|HD|M)720p?", regex.IGNORECASE), value("720p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"(?:BD|HD|M)480p?", regex.IGNORECASE), value("480p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"\b(?:4k|2160p|1080p|720p|480p)(?!.*\b(?:4k|2160p|1080p|720p|480p)\b)", regex.IGNORECASE), transform_resolution, {"remove": True})
    parser.add_handler("resolution", regex.compile(r"\b4k|21600?[pi]\b", regex.IGNORECASE), value("2160p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"(\d{3,4})[pi]", regex.IGNORECASE), value("$1p"), {"remove": True})
    parser.add_handler("resolution", regex.compile(r"(240|360|480|576|720|1080|2160|3840)[pi]", regex.IGNORECASE), lowercase, {"remove": True})

    # Date
    parser.add_handler("date", regex.compile(r"(?:\W|^)([[(]?(?:19[6-9]|20[012])[0-9]([. \-/\\])(?:0[1-9]|1[012])\2(?:0[1-9]|[12][0-9]|3[01])[])]?)(?:\W|$)"), date("YYYY MM DD"), {"remove": True})
    parser.add_handler("date", regex.compile(r"(?:\W|^)(\[?\]?(?:0[1-9]|[12][0-9]|3[01])([. \-/\\])(?:0[1-9]|1[012])\2(?:19[6-9]|20[01])[0-9][\])]?)(?:\W|$)"), date("DD MM YYYY"), {"remove": True})
    parser.add_handler("date", regex.compile(r"(?:\W)(\[?\]?(?:0[1-9]|1[012])([. \-/\\])(?:0[1-9]|[12][0-9]|3[01])\2(?:[0][1-9]|[0126789][0-9])[\])]?)(?:\W|$)"), date("MM DD YY"), {"remove": True})
    parser.add_handler("date", regex.compile(r"(?:\W)(\[?\]?(?:0[1-9]|[12][0-9]|3[01])([. \-/\\])(?:0[1-9]|1[012])\2(?:[0][1-9]|[0126789][0-9])[\])]?)(?:\W|$)"), date("DD MM YY"), {"remove": True})
    parser.add_handler(
        "date",
        regex.compile(r"(?:\W|^)([([]?(?:0?[1-9]|[12][0-9]|3[01])[. ]?(?:st|nd|rd|th)?([. \-/\\])(?:feb(?:ruary)?|jan(?:uary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sept?(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\2(?:19[7-9]|20[012])[0-9][)\]]?)(?=\W|$)", regex.IGNORECASE),
        date(["DD MMM YYYY", "Do MMM YYYY", "Do MMMM YYYY"]),
        {"remove": True},
    )
    parser.add_handler(
        "date",
        regex.compile(r"(?:\W|^)(\[?\]?(?:0?[1-9]|[12][0-9]|3[01])[. ]?(?:st|nd|rd|th)?([. \-\/\\])(?:feb(?:ruary)?|jan(?:uary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sept?(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\2(?:0[1-9]|[0126789][0-9])[\])]?)(?:\W|$)", regex.IGNORECASE),
        date("DD MMM YY"),
        {"remove": True},
    )
    parser.add_handler("date", regex.compile(r"(?:\W|^)(\[?\]?20[012][0-9](?:0[1-9]|1[012])(?:0[1-9]|[12][0-9]|3[01])[\])]?)(?:\W|$)"), date("YYYYMMDD"), {"remove": True})

    # Complete
    parser.add_handler("complete", regex.compile(r"\b((?:19\d|20[012])\d[ .]?-[ .]?(?:19\d|20[012])\d)\b"), boolean, {"remove": True})  # year range
    parser.add_handler("complete", regex.compile(r"[([][ .]?((?:19\d|20[012])\d[ .]?-[ .]?\d{2})[ .]?[)\]]"), boolean, {"remove": True})  # year range

    # Bit Rate
    parser.add_handler("bitrate", regex.compile(r"\b\d+[kmg]bps\b", regex.IGNORECASE), lowercase, {"remove": True})

    # Year
    parser.add_handler("year", regex.compile(r"\b(20[0-9]{2}|2100)(?!\D*\d{4}\b)"), integer, {"remove": True})
    parser.add_handler("year", regex.compile(r"[([]?(?!^)(?<!\d|Cap[. ]?)((?:19\d|20[012])\d)(?!\d|kbps)[)\]]?", regex.IGNORECASE), integer, {"remove": True})
    parser.add_handler("year", regex.compile(r"(?!^\w{4})^[([]?((?:19\d|20[012])\d)(?!\d|kbps)[)\]]?", regex.IGNORECASE), integer, {"remove": True})

    # Edition
    parser.add_handler("edition", regex.compile(r"\b\d{2,3}(th)?[\.\s\-\+_\/(),]Anniversary[\.\s\-\+_\/(),](Edition|Ed)?\b", regex.IGNORECASE), value("Anniversary Edition"), {"remove": True})
    parser.add_handler("edition", regex.compile(r"\bUltimate[\.\s\-\+_\/(),]Edition\b", regex.IGNORECASE), value("Ultimate Edition"), {"remove": True})
    parser.add_handler("edition", regex.compile(r"\bExtended[\.\s\-\+_\/(),]Director(\')?s\b", regex.IGNORECASE), value("Directors Cut"), {"remove": True})
    parser.add_handler("edition", regex.compile(r"\b(custom.?)?Extended\b", regex.IGNORECASE), value("Extended Edition"), {"remove": True})
    parser.add_handler("edition", regex.compile(r"\bDirector(\')?s.?Cut\b", regex.IGNORECASE), value("Directors Cut"), {"remove": True})
    parser.add_handler("edition", regex.compile(r"\bCollector(\')?s\b", regex.IGNORECASE), value("Collectors Edition"), {"remove": True})
    parser.add_handler("edition", regex.compile(r"\bTheatrical\b", regex.IGNORECASE), value("Theatrical"), {"remove": True})
    parser.add_handler("edition", regex.compile(r"\buncut(?!.gems)\b", regex.IGNORECASE), value("Uncut"), {"remove": True})
    parser.add_handler("edition", regex.compile(r"\bIMAX\b", regex.IGNORECASE), value("IMAX"), {"remove": True})
    parser.add_handler("edition", regex.compile(r"\b\.Diamond\.\b", regex.IGNORECASE), value("Diamond Edition"), {"remove": True})
    parser.add_handler("edition", regex.compile(r"\bRemaster(?:ed)?\b", regex.IGNORECASE), value("Remastered"), {"remove": True, "skipIfAlreadyFound": True})

    # Remastered
    parser.add_handler("remastered", regex.compile(r"\bRemaster(?:ed)?\b", regex.IGNORECASE), boolean, {"remove": True})

    # Documentary
    parser.add_handler("documentary", regex.compile(r"\bDOCU(?:menta?ry)?\b", regex.IGNORECASE), boolean, {"skipFromTitle": True})

    # Unrated
    parser.add_handler("unrated", regex.compile(r"\bunrated\b", regex.IGNORECASE), boolean, {"remove": True})

    # Uncensored
    parser.add_handler("uncensored", regex.compile(r"\buncensored\b", regex.IGNORECASE), boolean, {"remove": True})

    # Commentary
    parser.add_handler("commentary", regex.compile(r"\bcommentary\b", regex.IGNORECASE), boolean, {"remove": True})

    # Quality
    parser.add_handler("quality", regex.compile(r"\b(?:HD[ .-]*)?T(?:ELE)?S(?:YNC)?(?:Rip)?\b", regex.IGNORECASE), value("TeleSync"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\b(?:HD[ .-]*)?T(?:ELE)?C(?:INE)?(?:Rip)?\b"), value("TeleCine"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\b(?:DVD?|BD|BR|HD)?[ .-]*Scr(?:eener)?\b", regex.IGNORECASE), value("SCR"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bP(?:RE)?-?(HD|DVD)(?:Rip)?\b", regex.IGNORECASE), value("SCR"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bBlu[ .-]*Ray\b(?=.*remux)", regex.IGNORECASE), value("BluRay REMUX"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"(?:BD|BR|UHD)[- ]?remux", regex.IGNORECASE), value("BluRay REMUX"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"(?<=remux.*)\bBlu[ .-]*Ray\b", regex.IGNORECASE), value("BluRay REMUX"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bremux\b", regex.IGNORECASE), value("REMUX"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bBlu[ .-]*Ray\b(?![ .-]*Rip)", regex.IGNORECASE), value("BluRay"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bUHD[ .-]*Rip\b", regex.IGNORECASE), value("UHDRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bHD[ .-]*Rip\b", regex.IGNORECASE), value("HDRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bMicro[ .-]*HD\b", regex.IGNORECASE), value("HDRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\b(?:BR|Blu[ .-]*Ray)[ .-]*Rip\b", regex.IGNORECASE), value("BRRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bBD[ .-]*Rip\b|\bBDR\b|\bBD-RM\b|[[(]BD[\]) .,-]", regex.IGNORECASE), value("BDRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\b(?:HD[ .-]*)?DVD[ .-]*Rip\b", regex.IGNORECASE), value("DVDRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bVHS[ .-]*Rip?\b", regex.IGNORECASE), value("VHSRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bDVD(?:R\d?|.*Mux)?\b", regex.IGNORECASE), value("DVD"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bVHS\b", regex.IGNORECASE), value("VHS"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bPPVRip\b", regex.IGNORECASE), value("PPVRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bHD.?TV.?Rip\b", regex.IGNORECASE), value("HDTVRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bDVB[ .-]*(?:Rip)?\b", regex.IGNORECASE), value("HDTV"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bSAT[ .-]*Rips?\b", regex.IGNORECASE), value("SATRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bTVRips?\b", regex.IGNORECASE), value("TVRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bR5\b", regex.IGNORECASE), value("R5"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\b(?:DL|WEB|BD|BR)MUX\b", regex.IGNORECASE), value("WEBMux"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bWEB[ .-]*Rip\b", regex.IGNORECASE), value("WEBRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bWEB[ .-]?DL[ .-]?Rip\b", regex.IGNORECASE), value("WEB-DLRip"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bWEB[ .-]*(DL|.BDrip|.DLRIP)\b", regex.IGNORECASE), value("WEB-DL"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\b(?<!\w.)WEB\b|\bWEB(?!([ \.\-\(\],]+\d))\b", regex.IGNORECASE), value("WEB"), {"remove": True, "skipFromTitle": True})  #
    parser.add_handler("quality", regex.compile(r"\b(?:H[DQ][ .-]*)?CAM(?!.?(S|E|\()\d+)(?:H[DQ])?(?:[ .-]*Rip|Rp)?\b", regex.IGNORECASE), value("CAM"), {"remove": True, "skipFromTitle": True})  # can appear in a title as well, check it last
    parser.add_handler("quality", regex.compile(r"\b(?:H[DQ][ .-]*)?S[ \.\-]print", regex.IGNORECASE), value("CAM"), {"remove": True, "skipFromTitle": True})  # can appear in a title as well, check it last
    parser.add_handler("quality", regex.compile(r"\bPDTV\b", regex.IGNORECASE), value("PDTV"), {"remove": True})
    parser.add_handler("quality", regex.compile(r"\bHD(.?TV)?\b", regex.IGNORECASE), value("HDTV"), {"remove": True})

    # Video depth
    parser.add_handler("bit_depth", regex.compile(r"\bhevc\s?10\b", regex.IGNORECASE), value("10bit"))
    parser.add_handler("bit_depth", regex.compile(r"(?:8|10|12)[-\.]?(?=bit)", regex.IGNORECASE), value("$1bit"), {"remove": True})
    parser.add_handler("bit_depth", regex.compile(r"\bhdr10\b", regex.IGNORECASE), value("10bit"))
    parser.add_handler("bit_depth", regex.compile(r"\bhi10\b", regex.IGNORECASE), value("10bit"))

    def handle_bit_depth(context):
        result = context["result"]
        if "bit_depth" in result:
            # Replace hyphens and spaces with nothing (effectively removing them)
            result["bit_depth"] = result["bit_depth"].replace(" ", "").replace("-", "")

    parser.add_handler("bit_depth", handle_bit_depth)

    # Codec
    parser.add_handler("codec", regex.compile(r"\b[hx][\. \-]?264\b", regex.IGNORECASE), value("avc"), {"remove": True})
    parser.add_handler("codec", regex.compile(r"\b[hx][\. \-]?265\b", regex.IGNORECASE), value("hevc"), {"remove": True})
    parser.add_handler("codec", regex.compile(r"\bHEVC10(bit)?\b|\b[xh][\. \-]?265\b", regex.IGNORECASE), value("hevc"), {"remove": True})
    parser.add_handler("codec", regex.compile(r"\bhevc(?:\s?10)?\b", regex.IGNORECASE), value("hevc"), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("codec", regex.compile(r"\bdivx|xvid\b", regex.IGNORECASE), value("xvid"), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("codec", regex.compile(r"\bavc\b", regex.IGNORECASE), value("avc"), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("codec", regex.compile(r"\bav1\b", regex.IGNORECASE), value("av1"), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("codec", regex.compile(r"\b(?:mpe?g\d*)\b", regex.IGNORECASE), value("mpeg"), {"remove": True, "skipIfAlreadyFound": False})

    def handle_space_in_codec(context):
        if context["result"].get("codec"):
            context["result"]["codec"] = regex.sub("[ .-]", "", context["result"]["codec"])

    parser.add_handler("codec", handle_space_in_codec)

    # Channels
    parser.add_handler("channels", regex.compile(r"5[\.\s]1(ch)?\b", regex.IGNORECASE), uniq_concat(value("5.1")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("channels", regex.compile(r"\b(?:x[2-4]|5[\W]1(?:x[2-4])?)\b", regex.IGNORECASE), uniq_concat(value("5.1")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("channels", regex.compile(r"\b7[\.\- ]1(.?ch(annel)?)?\b", regex.IGNORECASE), uniq_concat(value("7.1")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("channels", regex.compile(r"\+?2[\.\s]0(?:x[2-4])?\b", regex.IGNORECASE), uniq_concat(value("2.0")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("channels", regex.compile(r"\b2\.0\b", regex.IGNORECASE), uniq_concat(value("2.0")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("channels", regex.compile(r"\bstereo\b", regex.IGNORECASE), uniq_concat(value("stereo")), {"remove": False, "skipIfAlreadyFound": False})
    parser.add_handler("channels", regex.compile(r"\bmono\b", regex.IGNORECASE), uniq_concat(value("mono")), {"remove": False, "skipIfAlreadyFound": False})

    # Audio
    parser.add_handler("audio", regex.compile(r"\b(?!.+HR)(DTS.?HD.?Ma(ster)?|DTS.?X)\b", regex.IGNORECASE), uniq_concat(value("DTS Lossless")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("audio", regex.compile(r"\bDTS(?!(.?HD.?Ma(ster)?|.X)).?(HD.?HR|HD)?\b", regex.IGNORECASE), uniq_concat(value("DTS Lossy")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("audio", regex.compile(r"\b(Dolby.?)?Atmos\b", regex.IGNORECASE), uniq_concat(value("Atmos")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("audio", regex.compile(r"\b(True[ .-]?HD|\.True\.)\b", regex.IGNORECASE), uniq_concat(value("TrueHD")), {"remove": True, "skipIfAlreadyFound": False, "skipFromTitle": True})
    parser.add_handler("audio", regex.compile(r"\bTRUE\b"), uniq_concat(value("TrueHD")), {"remove": True, "skipIfAlreadyFound": False, "skipFromTitle": True})
    parser.add_handler("audio", regex.compile(r"\bFLAC(?:\d\.\d)?(?:x\d+)?\b", regex.IGNORECASE), uniq_concat(value("FLAC")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("audio", regex.compile(r"DD2?[\+p]|DD Plus|Dolby Digital Plus|DDP5[ \.\_]1|EAC-?3", regex.IGNORECASE), uniq_concat(value("Dolby Digital Plus")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("audio", regex.compile(r"\b(DD|Dolby.?Digital|DolbyD|AC-?3(x2)?)\b", regex.IGNORECASE), uniq_concat(value("Dolby Digital")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("audio", regex.compile(r"\bQ?Q?AAC(x?2)?\b", regex.IGNORECASE), uniq_concat(value("AAC")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("audio", regex.compile(r"\bL?PCM\b", regex.IGNORECASE), uniq_concat(value("PCM")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("audio", regex.compile(r"\bOPUS(\b|\d)(?!.*[ ._-](\d{3,4}p))"), uniq_concat(value("OPUS")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("audio", regex.compile(r"\b(H[DQ])?.?(Clean.?Aud(io)?)\b", regex.IGNORECASE), uniq_concat(value("HQ Clean Audio")), {"remove": True, "skipIfAlreadyFound": False})

    # Group
    parser.add_handler("group", regex.compile(r"- ?(?!\d+$|S\d+|\d+x|ep?\d+|[^[]+]$)([^\-. []+[^\-. [)\]\d][^\-. [)\]]*)(?:\[[\w.-]+])?(?=\.\w{2,4}$|$)", regex.IGNORECASE), none, {"remove": False})

    # Volume
    parser.add_handler("volumes", regex.compile(r"\bvol(?:s|umes?)?[. -]*(?:\d{1,2}[., +/\\&-]+)+\d{1,2}\b", regex.IGNORECASE), range_func, {"remove": True})

    def handle_volumes(context):
        title = context["title"]
        result = context["result"]
        matched = context["matched"]

        start_index = matched.get("year", {}).get("match_index", 0)
        match = regex.search(r"\bvol(?:ume)?[. -]*(\d{1,2})", title[start_index:], regex.IGNORECASE)

        if match:
            matched["volumes"] = {"match": match.group(0), "match_index": match.start()}
            result["volumes"] = [int(match.group(1))]
            return {"raw_match": match.group(0), "match_index": match.start() + start_index, "remove": True}
        return None

    parser.add_handler("volumes", handle_volumes)

    # Pre-Language
    parser.add_handler("languages", regex.compile(r"\b(temporadas?|completa)\b", regex.IGNORECASE), uniq_concat(value("es")), {"skipIfAlreadyFound": False})

    # Country Code
    parser.add_handler("country", regex.compile(r"\b(US|UK|AU|NZ)\b"), value("$1"))

    # Languages (ISO 639-1 Standardized)
    parser.add_handler("languages", regex.compile(r"\bengl?(?:sub[A-Z]*)?\b", regex.IGNORECASE), uniq_concat(value("en")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\beng?sub[A-Z]*\b", regex.IGNORECASE), uniq_concat(value("en")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bing(?:l[eéê]s)?\b", regex.IGNORECASE), uniq_concat(value("en")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\besub\b", regex.IGNORECASE), uniq_concat(value("en")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\benglish\W+(?:subs?|sdh|hi)\b", regex.IGNORECASE), uniq_concat(value("en")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\beng?\b", regex.IGNORECASE), uniq_concat(value("en")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\benglish?\b", regex.IGNORECASE), uniq_concat(value("en")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:JP|JAP|JPN)\b", regex.IGNORECASE), uniq_concat(value("ja")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(japanese|japon[eê]s)\b", regex.IGNORECASE), uniq_concat(value("ja")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:KOR|kor[ .-]?sub)\b", regex.IGNORECASE), uniq_concat(value("ko")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(korean|coreano)\b", regex.IGNORECASE), uniq_concat(value("ko")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:traditional\W*chinese|chinese\W*traditional)(?:\Wchi)?\b", regex.IGNORECASE), uniq_concat(value("zh")), {"skipIfAlreadyFound": False, "remove": True})
    parser.add_handler("languages", regex.compile(r"\bzh-hant\b", regex.IGNORECASE), uniq_concat(value("zh")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:mand[ae]rin|ch[sn])\b", regex.IGNORECASE), uniq_concat(value("zh")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"(?<!shang-?)\bCH(?:I|T)\b", regex.IGNORECASE), uniq_concat(value("zh")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(chinese|chin[eê]s)\b", regex.IGNORECASE), uniq_concat(value("zh")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bzh-hans\b", regex.IGNORECASE), uniq_concat(value("zh")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bFR(?:a|e|anc[eê]s|VF[FQIB2]?)\b", regex.IGNORECASE), uniq_concat(value("fr")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b\[?(VF[FQRIB2]?\]?\b|(VOST)?FR2?)\b"), uniq_concat(value("fr")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(TRUE|SUB).?FRENCH\b|\bFRENCH\b|\bFre?\b"), uniq_concat(value("fr")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(VOST(?:FR?|A)?)\b", regex.IGNORECASE), uniq_concat(value("fr")), {"skipIfAlreadyFound": False})
    # parser.add_handler("languages", regex.compile(r"\b(VF[FQIB2]?|(TRUE|SUB).?FRENCH|(VOST)?FR2?)\b", regex.IGNORECASE), uniq_concat(value("fr")), {"remove": True, "skipIfAlreadyFound": True})
    parser.add_handler("languages", regex.compile(r"\bspanish\W?latin|american\W*(?:spa|esp?)", regex.IGNORECASE), uniq_concat(value("la")), {"skipFromTitle": True, "skipIfAlreadyFound": False, "remove": True})
    parser.add_handler("languages", regex.compile(r"\b(?:\bla\b.+(?:cia\b))", regex.IGNORECASE), uniq_concat(value("es")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:audio.)?lat(?:in?|ino)?\b", regex.IGNORECASE), uniq_concat(value("la")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:audio.)?(?:ESP?|spa|(en[ .]+)?espa[nñ]ola?|castellano)\b", regex.IGNORECASE), uniq_concat(value("es")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bes(?=[ .,/-]+(?:[A-Z]{2}[ .,/-]+){2,})\b", regex.IGNORECASE), uniq_concat(value("es")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?<=[ .,/-]+(?:[A-Z]{2}[ .,/-]+){2,})es\b", regex.IGNORECASE), uniq_concat(value("es")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?<=[ .,/-]+[A-Z]{2}[ .,/-]+)es(?=[ .,/-]+[A-Z]{2}[ .,/-]+)\b", regex.IGNORECASE), uniq_concat(value("es")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bes(?=\.(?:ass|ssa|srt|sub|idx)$)", regex.IGNORECASE), uniq_concat(value("es")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bspanish\W+subs?\b", regex.IGNORECASE), uniq_concat(value("es")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(spanish|espanhol)\b", regex.IGNORECASE), uniq_concat(value("es")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b[\.\s\[]?Sp[\.\s\]]?\b", regex.IGNORECASE), uniq_concat(value("es")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:p[rt]|en|port)[. (\\/-]*BR\b", regex.IGNORECASE), uniq_concat(value("pt")), {"skipIfAlreadyFound": False, "remove": True})
    parser.add_handler("languages", regex.compile(r"\bbr(?:a|azil|azilian)\W+(?:pt|por)\b", regex.IGNORECASE), uniq_concat(value("pt")), {"skipIfAlreadyFound": False, "remove": True})
    parser.add_handler("languages", regex.compile(r"\b(?:leg(?:endado|endas?)?|dub(?:lado)?|portugu[eèê]se?)[. -]*BR\b", regex.IGNORECASE), uniq_concat(value("pt")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bleg(?:endado|endas?)\b", regex.IGNORECASE), uniq_concat(value("pt")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bportugu[eèê]s[ea]?\b", regex.IGNORECASE), uniq_concat(value("pt")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bPT[. -]*(?:PT|ENG?|sub(?:s|titles?))\b", regex.IGNORECASE), uniq_concat(value("pt")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bpt(?=\.(?:ass|ssa|srt|sub|idx)$)", regex.IGNORECASE), uniq_concat(value("pt")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bPT\b", regex.IGNORECASE), uniq_concat(value("pt")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bpor\b", regex.IGNORECASE), uniq_concat(value("pt")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b-?ITA\b", regex.IGNORECASE), uniq_concat(value("it")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?<!w{3}\.\w+\.)IT(?=[ .,/-]+(?:[a-zA-Z]{2}[ .,/-]+){2,})\b"), uniq_concat(value("it")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bit(?=\.(?:ass|ssa|srt|sub|idx)$)", regex.IGNORECASE), uniq_concat(value("it")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bitaliano?\b", regex.IGNORECASE), uniq_concat(value("it")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bgreek[ .-]*(?:audio|lang(?:uage)?|subs?(?:titles?)?)?\b", regex.IGNORECASE), uniq_concat(value("el")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:GER|DEU)\b", regex.IGNORECASE), uniq_concat(value("de")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bde(?=[ .,/-]+(?:[A-Z]{2}[ .,/-]+){2,})\b", regex.IGNORECASE), uniq_concat(value("de")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?<=[ .,/-]+(?:[A-Z]{2}[ .,/-]+){2,})de\b", regex.IGNORECASE), uniq_concat(value("de")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?<=[ .,/-]+[A-Z]{2}[ .,/-]+)de(?=[ .,/-]+[A-Z]{2}[ .,/-]+)\b", regex.IGNORECASE), uniq_concat(value("de")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bde(?=\.(?:ass|ssa|srt|sub|idx)$)", regex.IGNORECASE), uniq_concat(value("de")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(german|alem[aã]o)\b", regex.IGNORECASE), uniq_concat(value("de")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bRUS?\b", regex.IGNORECASE), uniq_concat(value("ru")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(russian|russo)\b", regex.IGNORECASE), uniq_concat(value("ru")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bUKR\b", regex.IGNORECASE), uniq_concat(value("uk")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bukrainian\b", regex.IGNORECASE), uniq_concat(value("uk")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bhin(?:di)?\b", regex.IGNORECASE), uniq_concat(value("hi")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:(?<!w{3}\.\w+\.)tel(?!\W*aviv)|telugu)\b", regex.IGNORECASE), uniq_concat(value("te")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bt[aâ]m(?:il)?\b", regex.IGNORECASE), uniq_concat(value("ta")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:(?<!w{3}\.\w+\.)MAL(?:ay)?|malayalam)\b", regex.IGNORECASE), uniq_concat(value("ml")), {"remove": True, "skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:(?<!w{3}\.\w+\.)KAN(?:nada)?|kannada)\b", regex.IGNORECASE), uniq_concat(value("kn")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:(?<!w{3}\.\w+\.)MAR(?:a(?:thi)?)?|marathi)\b", regex.IGNORECASE), uniq_concat(value("mr")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:(?<!w{3}\.\w+\.)GUJ(?:arati)?|gujarati)\b", regex.IGNORECASE), uniq_concat(value("gu")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:(?<!w{3}\.\w+\.)PUN(?:jabi)?|punjabi)\b", regex.IGNORECASE), uniq_concat(value("pa")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:(?<!w{3}\.\w+\.)BEN(?!.\bThe|and|of\b)(?:gali)?|bengali)\b", regex.IGNORECASE), uniq_concat(value("bn")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?<!YTS\.)LT\b"), uniq_concat(value("lt")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\blithuanian\b", regex.IGNORECASE), uniq_concat(value("lt")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\blatvian\b", regex.IGNORECASE), uniq_concat(value("lv")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bestonian\b", regex.IGNORECASE), uniq_concat(value("et")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:(?<!w{3}\.\w+\.)PL|pol)\b", regex.IGNORECASE), uniq_concat(value("pl")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(polish|polon[eê]s|polaco)\b", regex.IGNORECASE), uniq_concat(value("pl")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(PLDUB|DUBPL|DubbingPL|LekPL|LektorPL)\b", regex.IGNORECASE), uniq_concat(value("pl")), {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bCZ[EH]?\b", regex.IGNORECASE), uniq_concat(value("cs")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bczech\b", regex.IGNORECASE), uniq_concat(value("cs")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bslo(?:vak|vakian|subs|[\]_)]?\.\w{2,4}$)\b", regex.IGNORECASE), uniq_concat(value("sk")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bHU\b"), uniq_concat(value("hu")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bHUN(?:garian)?\b", regex.IGNORECASE), uniq_concat(value("hu")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bROM(?:anian)?\b", regex.IGNORECASE), uniq_concat(value("ro")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bRO(?=[ .,/-]*(?:[A-Z]{2}[ .,/-]+)*sub)", regex.IGNORECASE), uniq_concat(value("ro")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bbul(?:garian)?\b", regex.IGNORECASE), uniq_concat(value("bg")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:srp|serbian)\b", regex.IGNORECASE), uniq_concat(value("sr")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:HRV|croatian)\b", regex.IGNORECASE), uniq_concat(value("hr")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bHR(?=[ .,/-]*(?:[A-Z]{2}[ .,/-]+)*sub)\b", regex.IGNORECASE), uniq_concat(value("hr")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bslovenian\b", regex.IGNORECASE), uniq_concat(value("sl")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:(?<!w{3}\.\w+\.)NL|dut|holand[eê]s)\b", regex.IGNORECASE), uniq_concat(value("nl")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bdutch\b", regex.IGNORECASE), uniq_concat(value("nl")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bflemish\b", regex.IGNORECASE), uniq_concat(value("nl")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:DK|danska|dansub|nordic)\b", regex.IGNORECASE), uniq_concat(value("da")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(danish|dinamarqu[eê]s)\b", regex.IGNORECASE), uniq_concat(value("da")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bdan\b(?=.*\.(?:srt|vtt|ssa|ass|sub|idx)$)", regex.IGNORECASE), uniq_concat(value("da")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:(?<!w{3}\.\w+\.|Sci-)FI|finsk|finsub|nordic)\b", regex.IGNORECASE), uniq_concat(value("fi")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bfinnish\b", regex.IGNORECASE), uniq_concat(value("fi")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:(?<!w{3}\.\w+\.)SE|swe|swesubs?|sv(?:ensk)?|nordic)\b", regex.IGNORECASE), uniq_concat(value("sv")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(swedish|sueco)\b", regex.IGNORECASE), uniq_concat(value("sv")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:NOR|norsk|norsub|nordic)\b", regex.IGNORECASE), uniq_concat(value("no")), {"skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(norwegian|noruegu[eê]s|bokm[aå]l|nob|nor(?=[\]_)]?\.\w{2,4}$))\b", regex.IGNORECASE), uniq_concat(value("no")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:arabic|[aá]rabe|ara)\b", regex.IGNORECASE), uniq_concat(value("ar")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\barab.*(?:audio|lang(?:uage)?|sub(?:s|titles?)?)\b", regex.IGNORECASE), uniq_concat(value("ar")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bar(?=\.(?:ass|ssa|srt|sub|idx)$)", regex.IGNORECASE), uniq_concat(value("ar")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:turkish|tur(?:co)?)\b", regex.IGNORECASE), uniq_concat(value("tr")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(TİVİBU|tivibu|bitturk(.net)?|turktorrent)\b", regex.IGNORECASE), uniq_concat(value("tr")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bvietnamese\b|\bvie(?=[\]_)]?\.\w{2,4}$)", regex.IGNORECASE), uniq_concat(value("vi")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bind(?:onesian)?\b", regex.IGNORECASE), uniq_concat(value("id")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(thai|tailand[eê]s)\b", regex.IGNORECASE), uniq_concat(value("th")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(THA|tha)\b"), uniq_concat(value("th")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(?:malay|may(?=[\]_)]?\.\w{2,4}$)|(?<=subs?\([a-z,]+)may)\b", regex.IGNORECASE), uniq_concat(value("ms")), {"skipIfFirst": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\bheb(?:rew|raico)?\b", regex.IGNORECASE), uniq_concat(value("he")), {"skipFromTitle": True, "skipIfAlreadyFound": False})
    parser.add_handler("languages", regex.compile(r"\b(persian|persa)\b", regex.IGNORECASE), uniq_concat(value("fa")), {"skipFromTitle": True, "skipIfAlreadyFound": False})

    parser.add_handler("languages", regex.compile(r"[\u3040-\u30ff]+", regex.IGNORECASE), uniq_concat(value("ja")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # japanese
    parser.add_handler("languages", regex.compile(r"[\u3400-\u4dbf]+", regex.IGNORECASE), uniq_concat(value("zh")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # chinese
    parser.add_handler("languages", regex.compile(r"[\u4e00-\u9fff]+", regex.IGNORECASE), uniq_concat(value("zh")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # chinese
    parser.add_handler("languages", regex.compile(r"[\uf900-\ufaff]+", regex.IGNORECASE), uniq_concat(value("zh")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # chinese
    parser.add_handler("languages", regex.compile(r"[\uff66-\uff9f]+", regex.IGNORECASE), uniq_concat(value("ja")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # japanese
    parser.add_handler("languages", regex.compile(r"[\u0400-\u04ff]+", regex.IGNORECASE), uniq_concat(value("ru")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # russian
    parser.add_handler("languages", regex.compile(r"[\u0600-\u06ff]+", regex.IGNORECASE), uniq_concat(value("ar")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # arabic
    parser.add_handler("languages", regex.compile(r"[\u0750-\u077f]+", regex.IGNORECASE), uniq_concat(value("ar")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # arabic
    parser.add_handler("languages", regex.compile(r"[\u0c80-\u0cff]+", regex.IGNORECASE), uniq_concat(value("kn")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # kannada
    parser.add_handler("languages", regex.compile(r"[\u0d00-\u0d7f]+", regex.IGNORECASE), uniq_concat(value("ml")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # malayalam
    parser.add_handler("languages", regex.compile(r"[\u0e00-\u0e7f]+", regex.IGNORECASE), uniq_concat(value("th")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # thai
    parser.add_handler("languages", regex.compile(r"[\u0900-\u097f]+", regex.IGNORECASE), uniq_concat(value("hi")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # hindi
    parser.add_handler("languages", regex.compile(r"[\u0980-\u09ff]+", regex.IGNORECASE), uniq_concat(value("bn")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # bengali
    parser.add_handler("languages", regex.compile(r"[\u0a00-\u0a7f]+", regex.IGNORECASE), uniq_concat(value("gu")), {"skipFromTitle": True, "skipIfAlreadyFound": False})  # gujarati

    def infer_language_based_on_naming(context):
        title = context["title"]
        result = context["result"]
        matched = context["matched"]
        if "languages" not in result or not any(lang in result["languages"] for lang in ["pt", "es"]):
            # Checking if episode naming convention suggests Portuguese language
            if (matched.get("episodes") and regex.search(r"capitulo|ao", matched["episodes"].get("raw_match", ""), regex.IGNORECASE)) or regex.search(r"dublado", title, regex.IGNORECASE):
                result["languages"] = result.get("languages", []) + ["pt"]

        return None

    parser.add_handler("languages", infer_language_based_on_naming)

    # Subbed
    parser.add_handler("subbed", regex.compile(r"\bmulti(?:ple)?[ .-]*(?:su?$|sub\w*|dub\w*)\b|msub", regex.IGNORECASE), boolean, {"remove": True})
    parser.add_handler("subbed", regex.compile(r"\b(?:Official.*?|Dual-?)?sub(s|bed)?\b", regex.IGNORECASE), boolean, {"remove": True})

    # Dubbed
    parser.add_handler("dubbed", regex.compile(r"[\[(\s]?\bmulti(?:ple)?[ .-]*(?:lang(?:uages?)?|audio|VF2)\b\][\[(\s]?", regex.IGNORECASE), boolean, {"remove": True, "skipIfAlreadyFound": False})
    parser.add_handler("dubbed", regex.compile(r"\btri(?:ple)?[ .-]*(?:audio|dub\w*)\b", regex.IGNORECASE), boolean, {"skipIfAlreadyFound": False})
    parser.add_handler("dubbed", regex.compile(r"\bdual[ .-]*(?:au?$|[aá]udio|line)\b", regex.IGNORECASE), boolean, {"skipIfAlreadyFound": False})
    parser.add_handler("dubbed", regex.compile(r"\bdual\b(?![ .-]*sub)", regex.IGNORECASE), boolean, {"skipIfAlreadyFound": False})
    parser.add_handler("dubbed", regex.compile(r"\b(fan\s?dub)\b", regex.IGNORECASE), boolean, {"remove": True, "skipFromTitle": True})
    parser.add_handler("dubbed", regex.compile(r"\b(Fan.*)?(?:DUBBED|dublado|dubbing|DUBS?)\b", regex.IGNORECASE), boolean, {"remove": True})
    parser.add_handler("dubbed", regex.compile(r"\b(?!.*\bsub(s|bed)?\b)([ _\-\[(\.])?(dual|multi)([ _\-\[(\.])?(audio)\b", regex.IGNORECASE), boolean, {"remove": True})
    parser.add_handler("dubbed", regex.compile(r"\b(JAP?(anese)?|ZH)\+ENG?(lish)?|ENG?(lish)?\+(JAP?(anese)?|ZH)\b", regex.IGNORECASE), boolean, {"remove": True})
    parser.add_handler("dubbed", regex.compile(r"\bMULTi\b", regex.IGNORECASE), boolean, {"remove": True})

    def handle_group(context):
        result = context["result"]
        matched = context["matched"]
        if "group" in matched and matched["group"].get("raw_match", "").startswith("[") and matched["group"]["raw_match"].endswith("]"):
            end_index = matched["group"]["match_index"] + len(matched["group"]["raw_match"]) if "group" in matched else 0

            # Check if there's any overlap with other matched elements
            if any(key != "group" and matched[key]["match_index"] < end_index for key in matched if "match_index" in matched[key]) and "group" in result:
                del result["group"]
        return None

    parser.add_handler("group", handle_group)

    # Size
    parser.add_handler("size", regex.compile(r"\b(\d+(\.\d+)?\s?(MB|GB|TB))\b", regex.IGNORECASE), none, {"remove": True})

    # Site
    parser.add_handler("site", regex.compile(r"\[([^\]]+\.[^\]]+)\](?=\.\w{2,4}$|\s)", regex.IGNORECASE), value("$1"), {"remove": True})
    parser.add_handler("site", regex.compile(r"\bwww.\w*.\w+\b", regex.IGNORECASE), value("$1"), {"remove": True})

    # Extension
    parser.add_handler("extension", regex.compile(r"\.(3g2|3gp|avi|flv|mkv|mk3d|mov|mp2|mp4|m4v|mpe|mpeg|mpg|mpv|webm|wmv|ogm|divx|ts|m2ts|iso|vob|sub|idx|ttxt|txt|smi|srt|ssa|ass|vtt|nfo|html)$", regex.IGNORECASE), lowercase)
    parser.add_handler("audio", regex.compile(r"\bMP3\b", regex.IGNORECASE), uniq_concat(value("MP3")), {"remove": True, "skipIfAlreadyFound": False})

    # Group
    parser.add_handler("group", regex.compile(r"\(([\w-]+)\)(?:$|\.\w{2,4}$)"))
    parser.add_handler("group", regex.compile(r"\b(INFLATE|DEFLATE)\b"), value("$1"), {"remove": True})
    parser.add_handler("group", regex.compile(r"\b(?:Erai-raws|Erai-raws\.com)\b", regex.IGNORECASE), value("Erai-raws"), {"remove": True})
    parser.add_handler("group", regex.compile(r"^\[([^[\]]+)]"))

    def handle_group_exclusion(context):
        result = context["result"]
        if "group" in result and result["group"] in ["-", ""]:
            del result["group"]
        return None

    parser.add_handler("group", handle_group_exclusion)
