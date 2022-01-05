import http from "../http-common";

export const getAll = () => {
  return http.get("/patients/");
};

export const get = id => {
  return http.get(`/patient/${id}`);
};

export const create = data => {
  return http.post("/create_patient/", data);
};

export const update = (id, data) => {
  return http.put(`/update_patient/${id}`, data);
};

export const remove = id => {
  return http.delete(`/delete_patient/${id}`);
};

export default {
  getAll,
  get,
  create,
  update,
  remove
};