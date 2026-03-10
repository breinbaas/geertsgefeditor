import streamlit as st
from math import inf


def analyze_gef(lines):
    result = {"startdate": None, "columninfos": [], "data_lines": []}
    for i, line in enumerate(lines):
        if line.find("#STARTDATE") == 0:
            result["startdate"] = line.split("=")[1].strip()
        elif line.find("#COLUMNINFO") == 0:
            result["columninfos"].append(
                {"index": len(result["columninfos"]), "min": inf, "max": -inf}
            )
        elif line.find("#EOH") == 0:
            start_data_lines = i + 1

    data_lines = []
    for line in lines[start_data_lines:]:
        args = [a.strip() for a in line.split(" ") if a.strip() != ""]
        if len(args) != len(result["columninfos"]):
            continue
        for i, arg in enumerate(args):
            try:
                arg = float(arg)
                if arg < result["columninfos"][i]["min"]:
                    result["columninfos"][i]["min"] = arg
                if arg > result["columninfos"][i]["max"]:
                    result["columninfos"][i]["max"] = arg
            except:
                continue
        data_str = ";".join(args)
        result["data_lines"].append(f"{data_str};!")

    return result


st.set_page_config(page_title="Geerts GEF Editor", page_icon="📝")

st.title("Geerts GEF Editor")
st.write(
    "Upload een `.gef` file. De app bewerkt de file om BRO compatibel te zijn waarna je het aangepaste bestand kunt downloaden."
)

uploaded_file = st.file_uploader(
    "Kies een .gef file", type=["gef"], accept_multiple_files=False
)

if uploaded_file is not None:
    st.success(
        f"Je hebt {uploaded_file.name} geüpload. Vul de bewerkingsopties in en klik op 'Genereer & Download'."
    )

    # Read the content of the uploaded file as text
    file_content = uploaded_file.getvalue().decode("utf-8")

    lines = [l.strip() for l in file_content.split("\n")]
    data = analyze_gef(lines)

    from datetime import datetime

    # Parse the startdate into a datetime object for the date pickers
    default_date = None
    if data["startdate"]:
        try:
            # GEF dates are typically 'yyyy, mm, dd' or similar, try catching variations
            # E.g. "2023, 11, 28"
            date_parts = [p.strip() for p in data["startdate"].split(",")]
            if len(date_parts) == 3:
                default_date = datetime(
                    int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
                ).date()
        except:
            pass  # Keep default None if it fails to parse

    with st.form("edit_form"):
        mtext_006 = st.selectbox("Sonderklasse", options=[1, 2, 3, 4, 5, 6, 7], index=0)

        mvar_012 = st.selectbox(
            "Sondeerklasse",
            options=[
                "mechanischDiscontinu",
                "mechanischContinu",
                "elektrischDiscontinu",
                "elektrischContinu",
            ],
            index=3,
        )

        mvar_017 = st.selectbox(
            "Stopcriterium",
            options=[
                "einddiepte",
                "wegdrukkracht",
                "conusweerstand",
                "wrijvingsweerstand",
                "waterspanning",
                "hellingshoek",
                "obstakel",
                "bezwijkrisico",
                "storing",
            ],
            index=0,
        )

        mtext_020 = st.radio(
            "signaalbewerking uitgevoerd",
            options=["Ja", "Nee"],
            index=1,
            horizontal=True,
        )

        mtext_021 = st.radio(
            "bewerking onderbrekingen uitgevoerd ",
            options=["Ja", "Nee"],
            index=0,
            horizontal=True,
        )

        mtext_101 = st.radio(
            "opdrachtgever",
            options=["Gemeente Amsterdam, 34366966", "Waterschap AGV, 34360267"],
            index=0,
            horizontal=True,
        )

        mtext_103 = st.radio(
            "kader inwinning",
            options=["waterkering", "bouwwerk en constructie"],
            index=0,
            horizontal=True,
        )

        mtext_105 = st.date_input(
            "datum locatiebepaling", value=default_date if default_date else "today"
        )
        mtext_107 = st.date_input(
            "datum verticale positiebepaling",
            value=default_date if default_date else "today",
        )

        mtext_109 = st.radio(
            "dissipatietest uitgevoerd", options=["Ja", "Nee"], index=1, horizontal=True
        )
        mtext_110 = st.radio(
            "expertcorrectie uitgevoerd",
            options=["Ja", "Nee"],
            index=1,
            horizontal=True,
        )
        mtext_111 = st.radio(
            "aanvullend onderzoek uitgevoerd",
            options=["Ja", "Nee"],
            index=1,
            horizontal=True,
        )

        mtext_112 = st.date_input("rapportagedatum onderzoek")
        mtext_113 = st.date_input("datum laatste bewerking")
        mtext_114 = st.date_input(
            "datum onderzoek", value=default_date if default_date else "today"
        )

        submitted_edit = st.form_submit_button("Genereer & Download")

    if submitted_edit:
        # Determine index of mvar_017 selection
        mvar_017_options = [
            "einddiepte",
            "wegdrukkracht",
            "conusweerstand",
            "wrijvingsweerstand",
            "waterspanning",
            "hellingshoek",
            "obstakel",
            "bezwijkrisico",
            "storing",
        ]
        mvar_017_idx = mvar_017_options.index(mvar_017)

        # Format the parameters based on form input
        mtext_006_fmt = f"6, 22476-1 / {mtext_006}, Test class"
        mvar_012_fmt = f"12, 0.000000, -, {mvar_012}"
        mvar_017_fmt = f"17, {mvar_017_idx}, -, Stop criteria"
        mtext_020_fmt = f"20, {mtext_020}, signaalbewerking uitgevoerd"
        mtext_021_fmt = f"21, {mtext_021}, bewerking onderbrekingen uitgevoerd"
        mtext_042_fmt = "42, MRG1, methode verticale positiebepaling"
        mtext_043_fmt = "43, LRG1, methode locatiebepaling"
        mtext_044_fmt = "44, ja, orientatie x as helling"
        mtext_101_fmt = f"101, {mtext_101}"
        mtext_102_fmt = "102, opdracht publieke taakuitvoering, kader aanlevering"
        mtext_103_fmt = f"103, {mtext_103}, kader inwinning"
        mtext_104_fmt = "104, Uitvoerder locatiebepaling, 41216593"
        mtext_106_fmt = "106, Uitvoerder verticale positiebepaling, 41216593"
        mtext_109_fmt = f"109, {mtext_109}, dissipatietest uitgevoerd"
        mtext_110_fmt = f"110, {mtext_110}, expertcorrectie uitgevoerd"
        mtext_111_fmt = f"111, {mtext_111}, aanvullend onderzoek uitgevoerd"
        mtext_115_fmt = "115, IMBRO, kwaliteitsregime"

        column_min_max_added = False
        new_file_lines = []
        for line in lines:
            if line.find("#FILEDATE=") == 0:
                new_file_lines.append(f"#FILEDATE= {data['startdate']}")
            elif line.find("#STARTTIME") == 0:
                new_file_lines.append("#STARTTIME= 00, 01, 00")
            elif line.find("#DATATYPE") == 0:
                new_file_lines.append("#DATATYPE= REALS")
                new_file_lines.append("#FIRSTSCAN= 1")

            elif line.find("#LASTSCAN") == 0 and not column_min_max_added:
                for i, ci in enumerate(data["columninfos"]):
                    new_file_lines.append(
                        f"#COLUMNMINMAX {i+1}, {ci['min']}, {ci['max']}"
                    )
                column_min_max_added = True
                new_file_lines.append("#COLUMNSEPARATOR= ;")
                new_file_lines.append("#RECORDSEPARATOR= !")
                new_file_lines.append(line)
            elif line.find("#EOH") == 0:
                new_file_lines.append("#EOH=")
                new_file_lines += data["data_lines"]
                break
            elif line.find("#MEASUREMENTTEXT= 6") == 0:
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_006_fmt}")
            elif line.find("#MEASUREMENTTEXT= 9") == 0:
                new_file_lines.append(line)
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_020_fmt}")
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_021_fmt}")
            elif line.find("#MEASUREMENTTEXT= 25") == 0:
                new_file_lines.append(line)
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_042_fmt}")
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_043_fmt}")
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_044_fmt}")
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_101_fmt}")
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_102_fmt}")
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_103_fmt}")
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_104_fmt}")
                new_file_lines.append(
                    f"#MEASUREMENTTEXT= 105, {mtext_105.strftime('%Y, %m, %d')}"
                )
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_106_fmt}")
                new_file_lines.append(
                    f"#MEASUREMENTTEXT= 107, {mtext_107.strftime('%Y, %m, %d')}"
                )
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_109_fmt}")
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_110_fmt}")
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_111_fmt}")
                new_file_lines.append(
                    f"#MEASUREMENTTEXT= 112, {mtext_112.strftime('%Y, %m, %d')}"
                )
                new_file_lines.append(
                    f"#MEASUREMENTTEXT= 113, {mtext_113.strftime('%Y, %m, %d')}"
                )
                new_file_lines.append(
                    f"#MEASUREMENTTEXT= 114, {mtext_114.strftime('%Y, %m, %d')}"
                )
                new_file_lines.append(f"#MEASUREMENTTEXT= {mtext_115_fmt}")
            elif line.find("#MEASUREMENTVAR= 12") == 0:
                new_file_lines.append(f"#MEASUREMENTVAR= {mvar_012_fmt}")
            elif line.find("#MEASUREMENTVAR= 17") == 0:
                new_file_lines.append(f"#MEASUREMENTVAR= {mvar_017_fmt}")
            else:
                new_file_lines.append(line)

        # Output logic
        file_content = "\n".join(new_file_lines)

        st.success("Het bestand is succesvol gegenereerd en klaar om te downloaden!")

        out_name = uploaded_file.name.replace(".gef", "_AANGEPAST.gef").replace(
            ".GEF", "_AANGEPAST.GEF"
        )

        st.download_button(
            label="Download Aangepaste GEF File",
            data=file_content,
            file_name=out_name,
            mime="text/plain",
            type="primary",
        )
