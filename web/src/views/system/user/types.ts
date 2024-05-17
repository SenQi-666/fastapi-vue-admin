export interface searchDataType {
  username?: string
  name?: string
  available?: string
}

export interface searchSelectDataType {
  name?: string
  available?: string
}

export interface tableDataType {
  id?: number;
  index?: number;
  username?: string;
  name?: string;
  email?: string;
  mobile?: string;
  gender?: number;
  password?: string;
  dept_id: number;
  dept_name?: string;
  roles?: Object;
  roleNames?: string;
  role_ids?: Object[];
  positions?: Object;
  positionNames?: string;
  position_ids?: Object[];
  is_superuser?: boolean;
  available?: boolean;
  description?: string;
  last_login?: string;
  created_at?: string;
  updated_at?: string;
  creator?: Object;
  creatorName?: string;
}