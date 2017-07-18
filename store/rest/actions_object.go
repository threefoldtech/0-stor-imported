package rest

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"

	log "github.com/Sirupsen/logrus"
	"github.com/gorilla/mux"
	"github.com/zero-os/0-stor/store/db"
	"github.com/zero-os/0-stor/store/rest/models"
)

// Createobject is the handler for POST /namespaces/{nsid}/objects
// Set an object into the namespace
func (api NamespacesAPI) Createobject(w http.ResponseWriter, r *http.Request) {
	var reqBody models.Object

	nsid := mux.Vars(r)["nsid"]

	ns := models.NamespaceCreate{
		Label: nsid,
	}

	exists, err := api.db.Exists(ns.Key())

	if err != nil {
		log.Errorln(err.Error())
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	if !exists {
		http.Error(w, "Namespace doesn't exist", http.StatusNotFound)
		return
	}

	// decode request
	defer r.Body.Close()
	if err := json.NewDecoder(r.Body).Decode(&reqBody); err != nil {
		log.Errorln(err.Error())
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}

	if err := reqBody.Validate(); err != nil {
		log.Errorln(err.Error())
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}

	contentSize := len([]byte(reqBody.Data))

	if contentSize <= 32{
		log.Errorf("Trying to create object with data size %d", contentSize)
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}

	// Make sure file contents are valid
	file, err := reqBody.ToFile(nsid)

	if err != nil {
		log.Errorln(err.Error())
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}



	oldFile := models.File{
		Id:        reqBody.Id,
		Namespace: nsid,
	}

	b, err := api.db.Get(oldFile.Key())

	if err != nil {
		if err != db.ErrNotFound {
			log.Errorln(err.Error())
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		} else {
			// New file created as oldFile not exists
			res := r.Context().Value("reservation")
			if res != nil{
				reservation := res.(*models.Reservation)
				if reservation.SizeRemaining() < file.Size() {
					http.Error(w, "File SizeAvailable exceeds the remaining free space in namespace", http.StatusForbidden)
					return
				}
				// TODO: Update reservation asynchronously
				reservation.SizeUsed += file.Size()

				b, err = reservation.Encode()

				if err != nil {
					log.Errorln(err.Error())
					http.Error(w, "Internal Server Error", http.StatusInternalServerError)
					return
				}

				if err := api.db.Set(reservation.Key(), b); err != nil {
					log.Errorln(err.Error())
					http.Error(w, "Internal Server Error", http.StatusInternalServerError)
					return
				}
			}

			b, err = file.Encode()
			if err != nil {
				log.Errorln(err.Error())
				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
				return
			}

			if err = api.db.Set(file.Key(), b); err != nil {
				log.Errorln(err.Error())
				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
				return
			}
		}
	} else {
		err = oldFile.Decode(b)
		if err != nil {
			log.Errorln(err.Error())
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}
		// Check files are identical, otherwise throw conflict
		if oldFile.CRC != file.CRC{
			http.Error(w, "File already exists with different content", http.StatusConflict)
			return
		}
		// Only update reference -- we don't update content here
		if oldFile.Reference < 255 {
			oldFile.Reference = oldFile.Reference + 1
			log.Debugln(file.Reference)
			b, err = oldFile.Encode()
			if err != nil {
				log.Errorln(err.Error())
				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
				return
			}

			if err = api.db.Set(oldFile.Key(), b); err != nil {
				log.Errorln(err.Error())
				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
				return
			}
		}

	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(&reqBody)
}

// DeleteObject is the handler for DELETE /namespaces/{nsid}/objects/{id}
// Delete object from the KV
func (api NamespacesAPI) DeleteObject(w http.ResponseWriter, r *http.Request) {
	nsid := mux.Vars(r)["nsid"]

	ns := models.NamespaceCreate{
		Label: nsid,
	}

	exists, err := api.db.Exists(ns.Key())

	if err != nil {
		log.Errorln(err.Error())
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	if !exists {
		http.Error(w, "Namespace doesn't exist", http.StatusNotFound)
		return
	}

	id := mux.Vars(r)["id"]

	f := models.File{
		Namespace: nsid,
		Id:        id,
	}

	v, err := api.db.Get(f.Key())

	if err != nil {
		if err == db.ErrNotFound{
			http.Error(w, "Namespace or object doesn't exist", http.StatusNotFound)
			return
		}
		log.Errorln(err.Error())
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}


	f = models.File{}
	if err := f.Decode(v); err != nil {
		log.Errorln(err.Error())
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	if f.Reference == 1{
		err = api.db.Delete(f.Key())

		if err != nil {
			log.Errorln(err.Error())
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}
		res := r.Context().Value("reservation")
		if res != nil{
			reservation := res.(*models.Reservation)
			reservation.SizeUsed -= f.Size()

			b, err := reservation.Encode()

			if err != nil {
				log.Errorln(err.Error())
				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
				return
			}
			if err := api.db.Set(reservation.Key(), b); err != nil {
				log.Errorln(err.Error())
				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
				return
			}
		}

	}else{
		f.Reference -= 1
		b, err := f.Encode()
		if err != nil{
			log.Errorln(err.Error())
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}
		err = api.db.Set(f.Key(), b)
		if err != nil{
			log.Errorln(err.Error())
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}
	}

	// 204 has no bddy
	http.Error(w, "", http.StatusNoContent)
}

// GetObject is the handler for GET /namespaces/{nsid}/objects/{id}
// Retrieve object from the KV
func (api NamespacesAPI) GetObject(w http.ResponseWriter, r *http.Request) {

	nsid := mux.Vars(r)["nsid"]

	ns := models.NamespaceCreate{
		Label: nsid,
	}

	exists, err := api.db.Exists(ns.Key())

	if err != nil {
		log.Errorln(err.Error())
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	if !exists {
		http.Error(w, "Namespace doesn't exist", http.StatusNotFound)
		return
	}

	id := mux.Vars(r)["id"]

	f := models.File{
		Namespace: nsid,
		Id:        id,
	}

	v, err := api.db.Get(f.Key())

	if err != nil {
		if err == db.ErrNotFound {
			http.Error(w, "object doesn't exist", http.StatusNotFound)
			return
		}
		log.Errorln(err.Error())
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	err = f.Decode(v)
	// Database Error
	if err != nil {
		log.Errorln(err.Error())
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	result, err := f.ToObject()
	if err != nil{
		log.Errorln(err.Error())
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return

	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(result)
}

// HeadObject is the handler for HEAD /namespaces/{nsid}/objects/{id}
// Tests object exists in the KV
func (api NamespacesAPI) HeadObject(w http.ResponseWriter, r *http.Request) {
	nsid := mux.Vars(r)["nsid"]

	ns := models.NamespaceCreate{
		Label: nsid,
	}

	exists, err := api.db.Exists(ns.Key())

	if err != nil {
		log.Errorln(err.Error())
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	if !exists {
		http.Error(w, "Namespace doesn't exist", http.StatusNotFound)
		return
	}

	id := mux.Vars(r)["id"]

	f := models.File{
		Namespace: nsid,
		Id:        id,
	}

	exists, err = api.db.Exists(f.Key())

	if err != nil {
		http.Error(w, "", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")

	if exists {
		w.WriteHeader(http.StatusOK)
		return
	}

	w.WriteHeader(http.StatusNotFound)
}

// Listobjects is the handler for GET /namespaces/{nsid}/objects
// List keys of the namespaces
func (api NamespacesAPI) Listobjects(w http.ResponseWriter, r *http.Request) {
	var respBody []models.Object

	// Pagination
	pageParam := r.FormValue("page")
	per_pageParam := r.FormValue("per_page")

	if pageParam == "" {
		pageParam = "1"
	}

	if per_pageParam == "" {
		per_pageParam = "20"
	}

	page, err := strconv.Atoi(pageParam)

	if err != nil {
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}

	per_page, err := strconv.Atoi(per_pageParam)

	if err != nil {
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}

	nsid := mux.Vars(r)["nsid"]

	ns := models.NamespaceCreate{
		Label: nsid,
	}

	exists, err := api.db.Exists(ns.Key())

	if err != nil {
		log.Errorln(err.Error())
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	if !exists {
		http.Error(w, "Namespace doesn't exist", http.StatusNotFound)
		return
	}

	startingIndex := (page-1)*per_page + 1
	resultsCount := per_page

	prefixStr := fmt.Sprintf("%s:", nsid)

	objects, err := api.db.Filter(prefixStr, startingIndex, resultsCount)

	if err != nil {
		log.Errorln(err.Error())
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	respBody = make([]models.Object, 0, len(objects))

	for _, record := range objects {
		f := new(models.File)
		if err := f.Decode(record); err != nil {
			log.Errorln("Error decoding namespace :%v", err)
			http.Error(w, "Error decoding namespace", http.StatusInternalServerError)
			return
		}

		o := models.Object{
			Id:   f.Id,
			Tags: f.Tags,
			Data: string(f.Payload),
		}

		respBody = append(respBody, o)
	}

	// return empty list if no results
	if len(respBody) == 0 {
		respBody = []models.Object{}
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(&respBody)
}
