export type Researchers = {
  id?: number;
  firstname: string;
  surname: string;
  img?: string;
  position: string;
  about: string;
  office?: string;
  email?: string;
  linkedin?: string;
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

export type ChatWithMessages = {
  chat: Chat;
  messages: Message[];
};

export type Chat = {
  id?: number;
  created?: Date;
};

export type Message = {
  id?: number;
  content: string;
  ai_response: boolean;
  created?: Date;
  chat?: number;
};

export type Email = {
  address: string;
  subject: string;
  message: string;
};
