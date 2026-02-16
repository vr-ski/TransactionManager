export interface Contractor {
  contractor_id: number;
  user_id: number;
  name: string;
}

// For creating a new contractor (POST /user/{user_id} expects name in body)
export interface ContractorCreate {
  name: string;
}
