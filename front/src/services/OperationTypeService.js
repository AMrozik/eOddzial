import http from "../http-common";

export const getAll = () => {
  return http.get("/operation_types/");
};

export const get = id => {
  return http.get(`/operation_type/${id}`);
};

export const create = data => {
  return http.post("/operation_types/", data);
};

export const update = (id, data) => {
  return http.put(`/operation_type/${id}`, data);
};

export const remove = id => {
  return http.delete(`/operation_type/${id}`);
};

export default {
  getAll,
  get,
  create,
  update,
  remove
};