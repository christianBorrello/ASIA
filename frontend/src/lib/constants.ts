import type { BodySystem } from "./types";

// Positions calibrated for SVG viewBox 500x300, head RIGHT, tail LEFT
// The container uses aspect-[5/3] with padding
export const BODY_SYSTEMS: BodySystem[] = [
  {
    id: "nervous",
    name_it: "Sistema nervoso",
    name_en: "Nervous system",
    emoji: "\u{1F9E0}",
    structures: ["Cervello", "Midollo spinale", "Nervi"],
    description: "Controlla tutte le funzioni del corpo e le risposte agli stimoli",
    position: { top: "12%", left: "80%" }, // inside the head
    color: "#8b5cf6",
  },
  {
    id: "sensory",
    name_it: "Organi di senso",
    name_en: "Sensory organs",
    emoji: "\u{1F443}",
    structures: ["Occhi (vista)", "Orecchie (udito)", "Naso (olfatto)", "Lingua (gusto)"],
    description: "Permettono al cane di percepire l\u2019ambiente",
    position: { top: "20%", left: "88%" }, // muzzle/nose area
    color: "#6366f1",
  },
  {
    id: "endocrine",
    name_it: "Sistema endocrino",
    name_en: "Endocrine system",
    emoji: "\u{1F9EC}",
    structures: ["Ghiandole endocrine (tiroide, surrenali, ecc.)"],
    description: "Produce ormoni che regolano molte funzioni corporee",
    position: { top: "28%", left: "73%" }, // neck (thyroid area)
    color: "#14b8a6",
  },
  {
    id: "immune",
    name_it: "Sistema immunitario (linfatico)",
    name_en: "Immune/Lymphatic system",
    emoji: "\u{1F6E1}\u{FE0F}",
    structures: ["Linfonodi", "Milza", "Vasi linfatici"],
    description: "Difende l\u2019organismo da infezioni e malattie",
    position: { top: "38%", left: "68%" }, // armpit/lymph node area
    color: "#22c55e",
  },
  {
    id: "respiratory",
    name_it: "Apparato respiratorio",
    name_en: "Respiratory system",
    emoji: "\u{1FAC1}",
    structures: ["Naso", "Trachea", "Bronchi", "Polmoni"],
    description: "Permette lo scambio di ossigeno e anidride carbonica",
    position: { top: "32%", left: "58%" }, // front thorax (lungs)
    color: "#06b6d4",
  },
  {
    id: "circulatory",
    name_it: "Apparato circolatorio",
    name_en: "Circulatory system",
    emoji: "\u{2764}\u{FE0F}",
    structures: ["Cuore", "Sangue", "Vasi sanguigni"],
    description: "Trasporta ossigeno, nutrienti e ormoni",
    position: { top: "42%", left: "55%" }, // center thorax (heart)
    color: "#ef4444",
  },
  {
    id: "integumentary",
    name_it: "Apparato tegumentario",
    name_en: "Integumentary system",
    emoji: "\u{1F9F4}",
    structures: ["Pelle", "Pelo", "Unghie"],
    description: "Protegge il corpo e regola la temperatura",
    position: { top: "22%", left: "48%" }, // dorsal/back area
    color: "#fb923c",
  },
  {
    id: "digestive",
    name_it: "Apparato digerente",
    name_en: "Digestive system",
    emoji: "\u{1F356}",
    structures: ["Bocca", "Esofago", "Stomaco", "Intestino tenue e crasso", "Fegato", "Pancreas"],
    description: "Trasforma il cibo in energia e nutrienti",
    position: { top: "48%", left: "44%" }, // abdomen center
    color: "#f59e0b",
  },
  {
    id: "urinary",
    name_it: "Apparato urinario",
    name_en: "Urinary system",
    emoji: "\u{1F6BD}",
    structures: ["Reni", "Ureteri", "Vescica", "Uretra"],
    description: "Elimina le sostanze di scarto e regola i liquidi",
    position: { top: "50%", left: "34%" }, // lower abdomen/kidney
    color: "#3b82f6",
  },
  {
    id: "reproductive",
    name_it: "Apparato riproduttore",
    name_en: "Reproductive system",
    emoji: "\u{1F43E}",
    structures: ["Organi sessuali"],
    description: "Permette la riproduzione",
    position: { top: "58%", left: "28%" }, // rear underside
    color: "#ec4899",
  },
  {
    id: "muscular",
    name_it: "Apparato muscolare",
    name_en: "Muscular system",
    emoji: "\u{1F4AA}",
    structures: ["Muscoli scheletrici", "Muscoli lisci", "Muscoli cardiaci"],
    description: "Permette movimento, postura e attivit\u00e0 interne",
    position: { top: "35%", left: "32%" }, // hind thigh/haunch
    color: "#d946ef",
  },
  {
    id: "skeletal",
    name_it: "Apparato scheletrico",
    name_en: "Skeletal system",
    emoji: "\u{1F9B4}",
    structures: ["Ossa", "Articolazioni", "Cartilagini"],
    description: "Sostiene il corpo e protegge gli organi",
    position: { top: "68%", left: "38%" }, // hind legs area
    color: "#a3a3a3",
  },
];

export const EVIDENCE_CONFIG: Record<string, { label: string; color: string; bg: string; border: string }> = {
  ALTO: { label: "Evidenza alta", color: "text-emerald-800", bg: "bg-emerald-50", border: "border-emerald-200" },
  MODERATO: { label: "Evidenza moderata", color: "text-amber-800", bg: "bg-amber-50", border: "border-amber-200" },
  BASSO: { label: "Evidenza bassa", color: "text-red-800", bg: "bg-red-50", border: "border-red-200" },
};
