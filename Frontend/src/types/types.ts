export type Researchers = {
  id?: number;
  firstname: string;
  surname: string;
  img?: string;
  position: string;
  about: string;
  email?: string;
  linkedIn?: string;
  keywords?: string;
  related_research?: string;
};

export type Events = {
  id?: number;
  name: string;
  date: string;
  img?: string;
  description: string;
  contact_email: string;
  location: string;
};

export type Research = {
  id?: number;
  name: string;
  summary?: string;
  source_file?: string;
  keywords?: string;
  researchers_related?: {
    id?: number;
    firstname: string;
    surname: string;
    img?: string;
  }[];
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
