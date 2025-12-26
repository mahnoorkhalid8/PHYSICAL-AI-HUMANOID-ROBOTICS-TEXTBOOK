// Extended user schema for personalization
export interface ExtendedUser {
  id: string;
  email: string;
  emailVerified: boolean;
  name?: string;
  image?: string;
  // Extended fields for personalization
  software_background: string;
  hardware_background: string;
  createdAt: Date;
  updatedAt: Date;
}

// Schema for user registration with background information
export interface UserRegistrationSchema {
  email: string;
  password: string;
  name?: string;
  // Required background information
  software_background: string;
  hardware_background: string;
}

// Validation rules for background fields
export const backgroundValidationRules = {
  software_background: {
    required: true,
    minLength: 2,
    maxLength: 200,
  },
  hardware_background: {
    required: true,
    minLength: 2,
    maxLength: 200,
  },
};