# Champs spécifiques du formulaire de devis, par prestation (FR, EN, AR).
# type : "select" (options) ou "text" / "number".
YN = (["Oui", "Non", "En cours"], ["Yes", "No", "In progress"], ["نعم", "لا", "قيد الإجراء"])
BIEN = (["Maison", "Appartement", "Local commercial", "Immeuble", "Terrain"],
        ["House", "Flat", "Shop", "Building", "Land"],
        ["مسكن", "شقة", "محل تجاري", "عمارة", "قطعة أرض"])
NIV = (["RDC", "R+1", "R+2", "R+3 et plus"], ["Ground floor", "1 upper floor", "2 upper floors", "3+ upper floors"],
       ["طابق أرضي", "طابق أرضي + 1", "طابق أرضي + 2", "طابق أرضي + 3 فأكثر"])
SURF = ("Surface approximative (m²)", "Approximate area (m²)", "المساحة التقريبية (م²)")

FIELDS = {
    "conception": [
        ("select", ("Type de projet", "Project type", "نوع المشروع"),
         (["Maison individuelle", "Immeuble", "Local commercial", "Équipement", "Autre"],
          ["Detached house", "Apartment building", "Shop", "Public facility", "Other"],
          ["سكن فردي", "عمارة", "محل تجاري", "مرفق", "أخرى"])),
        ("number", ("Surface du terrain (m²)", "Plot area (m²)", "مساحة قطعة الأرض (م²)"), None),
        ("select", ("Nombre de niveaux", "Number of storeys", "عدد الطوابق"), NIV),
        ("select", ("Acte ou livret foncier disponible ?", "Title deed available?", "هل لديكم عقد أو دفتر عقاري؟"), YN),
    ],
    "permis": [
        ("select", ("Acte demandé", "Document needed", "الوثيقة المطلوبة"),
         (["Permis de construire", "Certificat d'urbanisme", "Permis de démolir", "Permis de lotir ou morcellement"],
          ["Building permit", "Planning certificate", "Demolition permit", "Subdivision permit or certificate"],
          ["رخصة البناء", "شهادة التعمير", "رخصة الهدم", "رخصة التجزئة أو شهادة التقسيم"])),
        ("select", ("Avez-vous déjà des plans ?", "Do you already have plans?", "هل لديكم مخططات؟"),
         (["Non", "Oui, à mettre à jour", "Oui, complets"], ["No", "Yes, to update", "Yes, complete"], ["لا", "نعم، تحتاج تحيينًا", "نعم، كاملة"])),
        ("number", ("Surface à construire (m²)", "Floor area to build (m²)", "المساحة المراد بناؤها (م²)"), None),
    ],
    "chantier": [
        ("select", ("Stade du chantier", "Site stage", "مرحلة الورشة"),
         (["Pas encore commencé", "Fondations", "Gros œuvre", "Second œuvre", "Finitions"],
          ["Not started", "Foundations", "Structure", "Building services", "Finishes"],
          ["لم تنطلق بعد", "الأساسات", "الهيكل", "الأشغال الثانوية", "التشطيبات"])),
        ("select", ("Permis de construire obtenu ?", "Building permit obtained?", "هل تحصلتم على رخصة البناء؟"), YN),
        ("number", SURF, None),
    ],
    "conformite": [
        ("select", ("Situation de la construction", "Building situation", "وضعية البناية"),
         (["Achevée sans permis", "Achevée, non conforme au permis", "Inachevée avec permis", "Inachevée sans permis", "Certificat de conformité"],
          ["Completed without permit", "Completed, not matching permit", "Unfinished with permit", "Unfinished without permit", "Certificate of compliance"],
          ["مكتملة دون رخصة", "مكتملة وغير مطابقة للرخصة", "غير مكتملة برخصة", "غير مكتملة دون رخصة", "شهادة المطابقة"])),
        ("select", ("Nombre de niveaux", "Number of storeys", "عدد الطوابق"), NIV),
        ("number", ("Surface bâtie approximative (m²)", "Approximate built area (m²)", "المساحة المبنية التقريبية (م²)"), None),
    ],
    "expertise-amiable": [
        ("select", ("Objet de l'expertise", "Survey subject", "موضوع الخبرة"),
         (["Fissures", "Infiltration ou dégât des eaux", "État des lieux avant travaux du voisin", "Évaluation d'un bien", "Avis technique avant achat", "Autre"],
          ["Cracks", "Leak or water damage", "Condition report before neighbour's works", "Property valuation", "Technical opinion before purchase", "Other"],
          ["تشققات", "تسرب المياه أو رطوبة", "معاينة الحالة قبل أشغال الجار", "تقييم عقار", "رأي تقني قبل الشراء", "أخرى"])),
        ("select", ("Type de bien", "Property type", "نوع العقار"), BIEN),
        ("select", ("Urgence", "Urgency", "الاستعجال"),
         (["Urgent", "Dans le mois", "Pas urgent"], ["Urgent", "Within a month", "Not urgent"], ["مستعجل", "خلال الشهر", "غير مستعجل"])),
    ],
    "releve": [
        ("select", ("Type de bien", "Property type", "نوع العقار"), BIEN),
        ("number", SURF, None),
        ("select", ("Les plans serviront pour", "Plans needed for", "المخططات مطلوبة من أجل"),
         (["Vente", "Partage entre héritiers", "Dossier administratif", "Location", "Travaux"],
          ["Sale", "Inheritance division", "Administrative file", "Rental", "Works"],
          ["البيع", "القسمة بين الورثة", "ملف إداري", "الكراء", "الأشغال"])),
    ],
    "renovation": [
        ("select", ("Type de travaux", "Type of works", "نوع الأشغال"),
         (["Surélévation", "Extension", "Transformation en local", "Aménagement intérieur", "Façade", "Autre"],
          ["Extra storey", "Extension", "Conversion into a shop", "Interior design", "Facade", "Other"],
          ["تعلية", "توسعة", "تحويل إلى محل", "تهيئة داخلية", "واجهة", "أخرى"])),
        ("select", ("La construction existante a-t-elle un permis ?", "Does the existing building have a permit?", "هل للبناية القائمة رخصة؟"),
         (["Oui", "Non", "Je ne sais pas"], ["Yes", "No", "I don't know"], ["نعم", "لا", "لا أعلم"])),
        ("number", SURF, None),
    ],
    "public": [
        ("select", ("Maître d'ouvrage", "Client", "صاحب المشروع"),
         (["Direction de wilaya", "APC", "Office (OPGI...)", "Promoteur", "Autre"],
          ["Wilaya directorate", "Municipality (APC)", "Public office (OPGI...)", "Developer", "Other"],
          ["مديرية ولائية", "بلدية", "ديوان (OPGI...)", "مرقي", "أخرى"])),
        ("text", ("Objet (école, logements...)", "Subject (school, housing...)", "موضوع المشروع (مدرسة، سكنات...)"), None),
        ("text", ("Date limite de la consultation", "Submission deadline", "آخر أجل لإيداع العروض"), None),
    ],
}
