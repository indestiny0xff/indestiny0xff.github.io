"""Generate the two downloadable CVs (EN + FR) in modern single-column ATS style."""
import os

from fpdf import FPDF

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "cv")

# Segoe UI on Windows, Liberation Sans (metrically similar) elsewhere.
_FONT_CANDIDATES = [
    {
        "": r"C:\Windows\Fonts\segoeui.ttf",
        "B": r"C:\Windows\Fonts\segoeuib.ttf",
        "I": r"C:\Windows\Fonts\segoeuii.ttf",
    },
    {
        "": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "B": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "I": "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
    },
]
FONTS = next(f for f in _FONT_CANDIDATES if all(os.path.exists(p) for p in f.values()))

ACCENT = (109, 40, 217)      # purple, matches the site
TEXT = (26, 26, 30)
MUTED = (95, 95, 105)
RULE = (215, 210, 225)

M = 14                       # page margin (mm)
W = 210 - 2 * M              # usable width


class CV(FPDF):
    def __init__(self):
        super().__init__(format="A4")
        self.set_margins(M, M, M)
        self.set_auto_page_break(True, margin=12)
        self.add_font("Main", "", FONTS[""])
        self.add_font("Main", "B", FONTS["B"])
        self.add_font("Main", "I", FONTS["I"])
        self.set_font("Main", "", 9)

    def header_block(self, name, title):
        self.set_fill_color(*ACCENT)
        self.rect(0, 0, 210, 1.6, "F")
        self.set_text_color(*TEXT)
        self.set_font("Main", "B", 22)
        self.cell(0, 9, name, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Main", "B", 10.5)
        self.set_text_color(*ACCENT)
        self.cell(0, 5.5, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.4)

    def links_line(self, items, size=8.6):
        """One line of contact parts; (text, url, highlight). URLs are clickable."""
        sep = "  |  "
        h = 4.3
        for i, (txt, url, hot) in enumerate(items):
            if i:
                self.set_font("Main", "", size)
                self.set_text_color(*MUTED)
                self.cell(self.get_string_width(sep), h, sep)
            if url:
                self.set_font("Main", "B" if hot else "", size)
                self.set_text_color(*ACCENT)
                self.cell(self.get_string_width(txt) + 0.5, h, txt, link=url)
            else:
                self.set_font("Main", "", size)
                self.set_text_color(*MUTED)
                self.cell(self.get_string_width(txt) + 0.5, h, txt)
        self.ln(h)

    def section(self, label):
        self.ln(1.0)
        y = self.get_y()
        self.set_fill_color(*ACCENT)
        self.rect(M, y + 1.3, 2.4, 2.4, "F")
        self.set_font("Main", "B", 9.6)
        self.set_text_color(*ACCENT)
        self.set_x(M + 4.4)
        self.cell(0, 4.6, label.upper(), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*RULE)
        self.set_line_width(0.3)
        y = self.get_y() + 0.4
        self.line(M, y, 210 - M, y)
        self.ln(1.1)

    def para(self, text, size=8.8, color=TEXT, lh=3.7):
        self.set_font("Main", "", size)
        self.set_text_color(*color)
        self.multi_cell(W, lh, text, new_x="LMARGIN", new_y="NEXT")

    def role(self, title, org, meta):
        self.set_font("Main", "B", 9.4)
        self.set_text_color(*TEXT)
        self.cell(self.get_string_width(title) + 1, 4.5, title)
        self.set_font("Main", "", 9.4)
        self.set_text_color(*ACCENT)
        self.cell(0, 4.5, "· " + org, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Main", "I", 8.2)
        self.set_text_color(*MUTED)
        self.cell(0, 3.8, meta, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.4)

    def bullet(self, text):
        self.set_font("Main", "", 8.8)
        self.set_text_color(*TEXT)
        self.cell(4, 3.7, "-")
        self.multi_cell(W - 4, 3.7, text, new_x="LMARGIN", new_y="NEXT")

    def proj(self, name, desc):
        self.set_font("Main", "", 8.8)
        self.set_text_color(*TEXT)
        self.multi_cell(W, 3.7, f"**{name}** {desc}", markdown=True,
                        new_x="LMARGIN", new_y="NEXT")
        self.ln(0.5)

    def pub(self, title, note, url=None, hot=False):
        self.set_font("Main", "", 8.8)
        self.set_text_color(*TEXT)
        self.cell(4, 3.7, "-")
        if url:
            self.set_font("Main", "B" if hot else "", 8.8)
            self.set_text_color(*ACCENT)
            tw = self.get_string_width(title) + 1
            self.cell(tw, 3.7, title, link=url)
            self.set_font("Main", "", 8.8)
            self.set_text_color(*TEXT)
            self.multi_cell(W - 4 - tw, 3.7, " " + note, new_x="LMARGIN", new_y="NEXT")
        else:
            self.multi_cell(W - 4, 3.7, f"{title} {note}", new_x="LMARGIN", new_y="NEXT")

    def kv(self, key, val):
        self.set_font("Main", "B", 8.8)
        self.set_text_color(*TEXT)
        self.cell(38, 3.9, key)
        self.set_font("Main", "", 8.8)
        self.multi_cell(W - 38, 3.9, val, new_x="LMARGIN", new_y="NEXT")


def build_en():
    p = CV()
    p.add_page()
    p.header_block(
        "OTHMANE B.",
        "R&D Engineer · Cyber Threat Intelligence · Malware Analysis · Detection Engineering",
    )
    p.links_line([
        ("Paris, France", None, False),
        ("othmaneb@proton.me", "mailto:othmaneb@proton.me", False),
        ("Portfolio: indestiny0xff.github.io", "https://indestiny0xff.github.io/", True),
        ("Blog: indestiny0xff.github.io/blog", "https://indestiny0xff.github.io/blog/", False),
    ])
    p.links_line([
        ("github.com/indestiny0xff", "https://github.com/indestiny0xff", False),
        ("huntingbadguys.online", "https://huntingbadguys.online", False),
        ("x.com/indestiny_cti", "https://x.com/indestiny_cti", False),
    ])
    p.ln(0.8)

    p.section("Summary")
    p.para(
        "R&D engineer specialized in cyber threat intelligence, malware analysis and detection "
        "engineering, and creator of HuntingBadGuys, a threat infrastructure intelligence platform. "
        "Master's degree in Intelligence & Cyber Threats obtained in 2026. Seeking a technical CTI, "
        "malware analysis, detection engineering or blue team role from September 2026, in France or abroad."
    )

    p.section("Experience")
    p.role("R&D Engineer", "Gatewatcher", "Cyber Campus, Puteaux, France | Sep 2025 - Present")
    p.bullet("Designed a Suricata ruleset enrichment engine powered by LLMs and threat intelligence; "
             "it adds context and verdict guidance to every NDR alert and reduces manual triage effort "
             "for SOC analysts.")
    p.bullet("Conducted an applied study on LLMs and established a methodology for processing "
             "information efficiently with consistent, reliable results on business tasks; it now "
             "underpins the enrichment engine.")
    p.bullet("Automated the production of vulnerability monitoring reports on critical vulnerabilities, "
             "turning a multi-hour manual process into a repeatable pipeline delivered to clients.")
    p.bullet("Designed Suricata and YARA detection rules extending product coverage of current attacker "
             "tooling; produced threat actor intelligence reports feeding detection priorities and "
             "client briefings.")
    p.ln(1.0)
    p.role("CERT Analyst", "OWN Security", "Paris, France | Sep 2023 - Jul 2025")
    p.bullet("Drafted technical reports on APT and cybercrime campaigns, used directly by clients to "
             "adapt their defensive posture.")
    p.bullet("Ran strategic monitoring of ransomware and infostealer ecosystems, providing early "
             "visibility on emerging groups and tooling.")
    p.bullet("Performed malware analysis covering infection chains, obfuscation and encryption methods, "
             "and turned the findings into actionable intelligence.")
    p.bullet("Mapped cybercrime groups' infrastructure in support of long-term tracking and attribution.")
    p.ln(1.0)
    p.role("Security Automation Intern", "ORHUS", "Jul 2023 - Aug 2023")
    p.bullet("Analysed Google Workspace security processes (identity management, access controls, "
             "configuration baselines) and developed Python tooling automating configuration audits, "
             "policy enforcement checks and monitoring workflows.")
    p.bullet("Recommended security posture and architecture improvements focused on risk reduction, "
             "scalability and operational efficiency.")

    p.section("Projects")
    p.proj("HuntingBadGuys.",
           "([huntingbadguys.online](https://huntingbadguys.online)) "
           "Threat infrastructure intelligence platform designed and built end-to-end: 16+ concurrent "
           "collection modules (DNS, WHOIS, HTTP chains, Certificate Transparency, BGP/ASN, GeoIP), a "
           "65-pattern IOC extraction engine, binary analysis (hex, disassembly, decompilation, DIE), an "
           "AST-based query language, pHash/MinHash clustering, automated feeds (OpenPhish, URLhaus, "
           "ThreatFox) and one-click STIX 2.1 reports.")
    p.proj("CLICKFIX Analytics Platform (SEKOIA).",
           "Automates ClickFix infection-chain analysis from a single URL: static and dynamic analysis, "
           "VM execution, malware identification, and LLM reasoning with MCP integrations.")
    p.proj("CLAAR (Oteria team project).",
           "Collaborative anti-disinformation platform introducing Indicators of Disinformation (IODs); "
           "designed and integrated the browser extension collecting from TikTok, Telegram and websites "
           "through their APIs.")
    p.proj("Telegram Intelligence Collection.",
           "Automated monitoring of cybercriminal Telegram channels via the Telegram API, extracting "
           "aliases, wallets and infrastructure indicators; delivered the school talk \"Telegram OSINT 101\".")

    p.section("Publications & Research")
    p.pub("Research blog: indestiny0xff.github.io/blog",
          "· reverse engineering, malware analysis and threat research write-ups.",
          "https://indestiny0xff.github.io/blog/")
    p.pub("Data breach: the operations of Charming Kitten revealed",
          "· Gatewatcher Lab article.",
          "https://www.gatewatcher.com/en/lab/data-breach-the-operations-of-charming-kitten-revealed/")
    p.pub("Telegram OSINT 101",
          "· talk at Oteria Cyber School: tracking a cybercriminal group through the Telegram API.")

    p.section("Skills")
    p.kv("Languages", "Python, C, PowerShell, Bash, x86/x64 assembly")
    p.kv("Reverse engineering", "Ghidra, IDA, x32dbg/x64dbg, Windows/Linux kernel internals")
    p.kv("Detection", "Suricata, YARA, Sigma, KQL")
    p.kv("CTI & OSINT", "MISP, OpenCTI, Censys, Shodan, Urlscan, VirusTotal, API reverse engineering")
    p.kv("Systems & tooling", "Linux, Docker, Git, virtualization")

    p.section("Education & Certifications")
    p.kv("Master's degree", "Intelligence & Cyber Threats, Reverse Engineering specialization, "
                            "Oteria Cyber School, 2024-2026 (degree obtained)")
    p.kv("Certifications", "Windows Malware Analysis for Hedgehogs (Beginner) and Malware Analysis: "
                           "Intermediate to Expert, by @struppigel; TOEIC 930/990")
    p.kv("Spoken languages", "Arabic (native), French (fluent), English (advanced, TOEIC 930)")

    p.output(os.path.join(OUT_DIR, "OthmaneB_CV_EN.pdf"))
    return p.pages_count


def build_fr():
    p = CV()
    p.add_page()
    p.header_block(
        "OTHMANE B.",
        "Ingénieur R&D · Cyber Threat Intelligence · Analyse de malwares · Detection Engineering",
    )
    p.links_line([
        ("Paris, France", None, False),
        ("othmaneb@proton.me", "mailto:othmaneb@proton.me", False),
        ("Portfolio: indestiny0xff.github.io", "https://indestiny0xff.github.io/", True),
        ("Blog : indestiny0xff.github.io/blog", "https://indestiny0xff.github.io/blog/", False),
    ])
    p.links_line([
        ("github.com/indestiny0xff", "https://github.com/indestiny0xff", False),
        ("huntingbadguys.online", "https://huntingbadguys.online", False),
        ("x.com/indestiny_cti", "https://x.com/indestiny_cti", False),
    ])
    p.ln(0.8)

    p.section("Profil")
    p.para(
        "Ingénieur R&D spécialisé en cyber threat intelligence, analyse de malwares et detection "
        "engineering, créateur de HuntingBadGuys, une plateforme de threat infrastructure intelligence. "
        "Mastère Renseignement & Cybermenace obtenu en 2026. Recherche un poste technique en CTI, analyse "
        "de malwares, detection engineering ou blue team à partir de septembre 2026, en France ou à l'étranger."
    )

    p.section("Expérience professionnelle")
    p.role("Ingénieur R&D", "Gatewatcher", "Cyber Campus, Puteaux, France | Sept 2025 - Aujourd'hui")
    p.bullet("Conception d'un moteur d'enrichissement de rulesets Suricata basé sur les LLMs et la threat "
             "intelligence ; il ajoute contexte et aide au verdict à chaque alerte NDR et réduit l'effort "
             "de triage manuel des analystes SOC.")
    p.bullet("Réalisation d'une étude appliquée sur les LLMs et mise en place d'une méthodologie de "
             "traitement efficace de l'information produisant des résultats cohérents et fiables sur des "
             "tâches métier ; elle sous-tend aujourd'hui le moteur d'enrichissement.")
    p.bullet("Automatisation des rapports de veille sur les vulnérabilités critiques, transformant un "
             "processus manuel de plusieurs heures en pipeline reproductible livré aux clients.")
    p.bullet("Conception de règles de détection Suricata et YARA étendant la couverture du produit ; "
             "rédaction de rapports de renseignement sur les acteurs de la menace alimentant priorités de "
             "détection et briefings clients.")
    p.ln(1.0)
    p.role("Analyste CERT", "OWN Security", "Paris, France | Sept 2023 - Juil 2025")
    p.bullet("Rédaction de rapports techniques sur les campagnes APT et cybercriminelles, utilisés "
             "directement par les clients pour adapter leur posture défensive.")
    p.bullet("Veille stratégique sur les écosystèmes ransomware et infostealer, donnant une visibilité "
             "précoce sur les groupes et outils émergents.")
    p.bullet("Analyse technique de malwares : chaînes d'infection, obfuscation et méthodes de chiffrement, "
             "avec transformation des résultats en renseignement actionnable.")
    p.bullet("Cartographie de l'infrastructure des groupes cybercriminels en soutien au tracking de long "
             "terme et à l'attribution.")
    p.ln(1.0)
    p.role("Stagiaire en automatisation sécurité", "ORHUS", "Juil 2023 - Août 2023")
    p.bullet("Audit de sécurité d'un environnement Google Workspace (identités, contrôles d'accès, "
             "configurations) avec développement d'outils Python automatisant audits, contrôles de "
             "politiques et supervision, et recommandations d'améliorations de la posture de sécurité.")

    p.section("Projets")
    p.proj("HuntingBadGuys.",
           "([huntingbadguys.online](https://huntingbadguys.online)) "
           "Plateforme de threat infrastructure intelligence conçue et développée de bout en bout : 16+ "
           "modules de collecte concurrents (DNS, WHOIS, chaînes HTTP, Certificate Transparency, BGP/ASN, "
           "GeoIP), moteur d'extraction d'IOCs à 65 patterns, analyse binaire (hex, désassemblage, "
           "décompilation, DIE), langage de requête basé AST, clustering pHash/MinHash, feeds automatisés "
           "(OpenPhish, URLhaus, ThreatFox) et rapports STIX 2.1 en un clic.")
    p.proj("CLICKFIX Analytics Platform (SEKOIA).",
           "Automatise l'analyse des chaînes d'infection ClickFix à partir d'une URL : analyses statique "
           "et dynamique, exécution en VM, identification du malware, raisonnement LLM avec intégrations MCP.")
    p.proj("CLAAR (projet d'équipe, Oteria).",
           "Plateforme collaborative de lutte contre la désinformation introduisant les Indicators of "
           "Disinformation (IODs) ; conception et intégration de l'extension navigateur collectant depuis "
           "TikTok, Telegram et les sites web via leurs APIs.")
    p.proj("Collecte d'intelligence sur Telegram.",
           "Surveillance automatisée de canaux cybercriminels via l'API Telegram, avec extraction d'alias, "
           "de wallets et d'indicateurs d'infrastructure ; présentation « Telegram OSINT 101 » à l'école.")

    p.section("Publications & Recherche")
    p.pub("Blog de recherche : indestiny0xff.github.io/blog",
          "· write-ups de reverse engineering, d'analyse de malwares et de threat research.",
          "https://indestiny0xff.github.io/blog/")
    p.pub("Data breach: the operations of Charming Kitten revealed",
          "· article Gatewatcher Lab.",
          "https://www.gatewatcher.com/en/lab/data-breach-the-operations-of-charming-kitten-revealed/")
    p.pub("Telegram OSINT 101",
          "· présentation à Oteria Cyber School : tracking d'un groupe cybercriminel via l'API Telegram.")

    p.section("Compétences")
    p.kv("Langages", "Python, C, PowerShell, Bash, assembleur x86/x64")
    p.kv("Reverse engineering", "Ghidra, IDA, x32dbg/x64dbg, internals kernel Windows/Linux")
    p.kv("Détection", "Suricata, YARA, Sigma, KQL")
    p.kv("CTI & OSINT", "MISP, OpenCTI, Censys, Shodan, Urlscan, VirusTotal, reverse d'API")
    p.kv("Systèmes & outils", "Linux, Docker, Git, virtualisation")

    p.section("Formation & Certifications")
    p.kv("Mastère", "Renseignement & Cybermenace, spécialisation Reverse Engineering, "
                    "Oteria Cyber School, 2024-2026 (diplôme obtenu)")
    p.kv("Certifications", "Windows Malware Analysis for Hedgehogs (Beginner) et Malware Analysis: "
                           "Intermediate to Expert, par @struppigel ; TOEIC 930/990")
    p.kv("Langues", "Arabe (natif), Français (courant), Anglais (avancé, TOEIC 930)")

    p.output(os.path.join(OUT_DIR, "OthmaneB_CV_FR.pdf"))
    return p.pages_count


os.makedirs(OUT_DIR, exist_ok=True)
print("EN pages:", build_en())
print("FR pages:", build_fr())
print("done")
