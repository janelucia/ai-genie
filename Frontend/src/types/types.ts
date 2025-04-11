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

export type Chat = {
  chat: {
    id?: number;
    created?: Date;
  };
  messages: Message[];
};

export type Message = {
  id?: number;
  content: string;
  ai_response: boolean;
  created?: Date;
  chat?: number;
};
