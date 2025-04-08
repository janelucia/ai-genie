export type Researchers = {
  id: number;
  firstname: string;
  surname: string;
  related_research: number;
};

export type Events = {
  id: number;
  name: string;
  date: string;
};

export type Research = {
  id: number;
  name: string;
  summary: string;
  source_file: string;
};

export type ChatMessage = {
  text: string;
  sender: "you" | "bot";
  timestamp: string;
};
