package grpc

import (
	"bytes"

	log "github.com/Sirupsen/logrus"

	"golang.org/x/net/context"

	pb "github.com/zero-os/0-stor/grpc_store"
	"github.com/zero-os/0-stor/server/db"
	"github.com/zero-os/0-stor/server/manager"
	"github.com/zero-os/0-stor/server/stats"
)

var _ (pb.ObjectManagerServer) = (*ObjectAPI)(nil)

type ObjectAPI struct {
	db db.DB
}

func NewObjectAPI(db db.DB) *ObjectAPI {
	return &ObjectAPI{
		db: db,
	}
}

func (api *ObjectAPI) Create(ctx context.Context, req *pb.CreateObjectRequest) (*pb.CreateObjectReply, error) {
	label := req.GetLabel()

	// increase request counter
	go stats.IncrWrite(label)

	if err := validateJWT(ctx, MethodWrite, label); err != nil {
		return nil, err
	}

	obj := req.GetObject()

	mgr := manager.NewObjectManager(label, api.db)

	if err := mgr.Set([]byte(obj.GetKey()), obj.GetValue(), obj.GetReferenceList()); err != nil {
		return nil, err
	}

	return &pb.CreateObjectReply{}, nil
}

func (api *ObjectAPI) List(req *pb.ListObjectsRequest, stream pb.ObjectManager_ListServer) error {

	label := req.GetLabel()

	// increase rate counter
	go stats.IncrRead(label)

	if err := validateJWT(stream.Context(), MethodRead, label); err != nil {
		log.Debugln("validated failed", err)
		return err
	}

	mgr := manager.NewObjectManager(label, api.db)

	keys, err := mgr.List(0, -1)
	if err != nil {
		return err
	}

	for _, key := range keys {
		obj, err := mgr.Get(key)
		if err != nil {
			return err
		}

		if err := stream.Send(grpcObj(string(key), obj)); err != nil {
			return nil
		}
	}

	return nil
}
func (api *ObjectAPI) Get(ctx context.Context, req *pb.GetObjectRequest) (*pb.GetObjectReply, error) {
	label, key := req.GetLabel(), req.GetKey()

	if err := validateJWT(ctx, MethodRead, label); err != nil {
		return nil, err
	}

	// increase rate counter
	go stats.IncrRead(label)

	mgr := manager.NewObjectManager(label, api.db)

	obj, err := mgr.Get([]byte(key))
	if err != nil {
		return nil, err
	}

	resp := &pb.GetObjectReply{
		Object: grpcObj(key, obj),
	}

	return resp, nil
}

func (api *ObjectAPI) Exists(ctx context.Context, req *pb.ExistsObjectRequest) (*pb.ExistsObjectReply, error) {
	label, key := req.GetLabel(), req.GetKey()

	// increase rate counter
	go stats.IncrRead(label)

	if err := validateJWT(ctx, MethodRead, label); err != nil {
		return nil, err
	}

	mgr := manager.NewObjectManager(label, api.db)

	exists, err := mgr.Exists([]byte(key))
	if err != nil {
		return nil, err
	}

	return &pb.ExistsObjectReply{
		Exists: exists,
	}, nil
}

func (api *ObjectAPI) Delete(ctx context.Context, req *pb.DeleteObjectRequest) (*pb.DeleteObjectReply, error) {
	label, key := req.GetLabel(), req.GetKey()

	// increase rate counter
	go stats.IncrWrite(label)

	if err := validateJWT(ctx, MethodDelete, label); err != nil {
		return nil, err
	}

	mgr := manager.NewObjectManager(label, api.db)

	if err := mgr.Delete([]byte(key)); err != nil {
		return nil, err
	}

	return &pb.DeleteObjectReply{}, nil
}

// grpcObj convert a db.Object to a pb.Object
func grpcObj(key string, in *db.Object) (out *pb.Object) {
	out = &pb.Object{
		Key:           key,
		Value:         in.Data,
		ReferenceList: make([]string, 0, db.RefIDCount),
	}

	for i := range in.ReferenceList {
		bRef := bytes.Trim(in.ReferenceList[i][:], "\x00")
		if len(bRef) == 0 {
			continue
		}
		out.ReferenceList = append(out.ReferenceList, string(bRef))
	}
	return
}
