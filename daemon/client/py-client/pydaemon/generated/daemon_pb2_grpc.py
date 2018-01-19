# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import daemon_pb2 as daemon__pb2


class NamespaceServiceStub(object):
  """NamespaceService is the service to be used to manage namespaces
  and the permissions of users linked to those namespaces.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CreateNamespace = channel.unary_unary(
        '/schema.NamespaceService/CreateNamespace',
        request_serializer=daemon__pb2.CreateNamespaceRequest.SerializeToString,
        response_deserializer=daemon__pb2.CreateNamespaceResponse.FromString,
        )
    self.DeleteNamespace = channel.unary_unary(
        '/schema.NamespaceService/DeleteNamespace',
        request_serializer=daemon__pb2.DeleteNamespaceRequest.SerializeToString,
        response_deserializer=daemon__pb2.DeleteNamespaceResponse.FromString,
        )
    self.SetPermission = channel.unary_unary(
        '/schema.NamespaceService/SetPermission',
        request_serializer=daemon__pb2.SetPermissionRequest.SerializeToString,
        response_deserializer=daemon__pb2.SetPermissionResponse.FromString,
        )
    self.GetPermission = channel.unary_unary(
        '/schema.NamespaceService/GetPermission',
        request_serializer=daemon__pb2.GetPermissionRequest.SerializeToString,
        response_deserializer=daemon__pb2.GetPermissionResponse.FromString,
        )


class NamespaceServiceServicer(object):
  """NamespaceService is the service to be used to manage namespaces
  and the permissions of users linked to those namespaces.
  """

  def CreateNamespace(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteNamespace(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetPermission(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetPermission(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_NamespaceServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CreateNamespace': grpc.unary_unary_rpc_method_handler(
          servicer.CreateNamespace,
          request_deserializer=daemon__pb2.CreateNamespaceRequest.FromString,
          response_serializer=daemon__pb2.CreateNamespaceResponse.SerializeToString,
      ),
      'DeleteNamespace': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteNamespace,
          request_deserializer=daemon__pb2.DeleteNamespaceRequest.FromString,
          response_serializer=daemon__pb2.DeleteNamespaceResponse.SerializeToString,
      ),
      'SetPermission': grpc.unary_unary_rpc_method_handler(
          servicer.SetPermission,
          request_deserializer=daemon__pb2.SetPermissionRequest.FromString,
          response_serializer=daemon__pb2.SetPermissionResponse.SerializeToString,
      ),
      'GetPermission': grpc.unary_unary_rpc_method_handler(
          servicer.GetPermission,
          request_deserializer=daemon__pb2.GetPermissionRequest.FromString,
          response_serializer=daemon__pb2.GetPermissionResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'schema.NamespaceService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class FileServiceStub(object):
  """FileService is the service to be used to write, read, delete, check and repair files.
  The fileService follows the principle of everything is a file.
  All files are written as raw binary data, but also have
  metadata bound to them, which identify where and how they are stored.
  This metadata is returned, when creating or altering the metadata,
  however if not needed for anything it can be ignored, as it is stored by the daemon (server),
  already, using the underlying metastor client.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Write = channel.unary_unary(
        '/schema.FileService/Write',
        request_serializer=daemon__pb2.WriteRequest.SerializeToString,
        response_deserializer=daemon__pb2.WriteResponse.FromString,
        )
    self.WriteFile = channel.unary_unary(
        '/schema.FileService/WriteFile',
        request_serializer=daemon__pb2.WriteFileRequest.SerializeToString,
        response_deserializer=daemon__pb2.WriteFileResponse.FromString,
        )
    self.WriteStream = channel.stream_unary(
        '/schema.FileService/WriteStream',
        request_serializer=daemon__pb2.WriteStreamRequest.SerializeToString,
        response_deserializer=daemon__pb2.WriteStreamResponse.FromString,
        )
    self.Read = channel.unary_unary(
        '/schema.FileService/Read',
        request_serializer=daemon__pb2.ReadRequest.SerializeToString,
        response_deserializer=daemon__pb2.ReadResponse.FromString,
        )
    self.ReadFile = channel.unary_unary(
        '/schema.FileService/ReadFile',
        request_serializer=daemon__pb2.ReadFileRequest.SerializeToString,
        response_deserializer=daemon__pb2.ReadFileResponse.FromString,
        )
    self.ReadStream = channel.unary_stream(
        '/schema.FileService/ReadStream',
        request_serializer=daemon__pb2.ReadStreamRequest.SerializeToString,
        response_deserializer=daemon__pb2.ReadStreamResponse.FromString,
        )
    self.Delete = channel.unary_unary(
        '/schema.FileService/Delete',
        request_serializer=daemon__pb2.DeleteRequest.SerializeToString,
        response_deserializer=daemon__pb2.DeleteResponse.FromString,
        )
    self.Check = channel.unary_unary(
        '/schema.FileService/Check',
        request_serializer=daemon__pb2.CheckRequest.SerializeToString,
        response_deserializer=daemon__pb2.CheckResponse.FromString,
        )
    self.Repair = channel.unary_unary(
        '/schema.FileService/Repair',
        request_serializer=daemon__pb2.RepairRequest.SerializeToString,
        response_deserializer=daemon__pb2.RepairResponse.FromString,
        )


class FileServiceServicer(object):
  """FileService is the service to be used to write, read, delete, check and repair files.
  The fileService follows the principle of everything is a file.
  All files are written as raw binary data, but also have
  metadata bound to them, which identify where and how they are stored.
  This metadata is returned, when creating or altering the metadata,
  however if not needed for anything it can be ignored, as it is stored by the daemon (server),
  already, using the underlying metastor client.
  """

  def Write(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def WriteFile(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def WriteStream(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Read(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReadFile(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReadStream(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Delete(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Check(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Repair(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_FileServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Write': grpc.unary_unary_rpc_method_handler(
          servicer.Write,
          request_deserializer=daemon__pb2.WriteRequest.FromString,
          response_serializer=daemon__pb2.WriteResponse.SerializeToString,
      ),
      'WriteFile': grpc.unary_unary_rpc_method_handler(
          servicer.WriteFile,
          request_deserializer=daemon__pb2.WriteFileRequest.FromString,
          response_serializer=daemon__pb2.WriteFileResponse.SerializeToString,
      ),
      'WriteStream': grpc.stream_unary_rpc_method_handler(
          servicer.WriteStream,
          request_deserializer=daemon__pb2.WriteStreamRequest.FromString,
          response_serializer=daemon__pb2.WriteStreamResponse.SerializeToString,
      ),
      'Read': grpc.unary_unary_rpc_method_handler(
          servicer.Read,
          request_deserializer=daemon__pb2.ReadRequest.FromString,
          response_serializer=daemon__pb2.ReadResponse.SerializeToString,
      ),
      'ReadFile': grpc.unary_unary_rpc_method_handler(
          servicer.ReadFile,
          request_deserializer=daemon__pb2.ReadFileRequest.FromString,
          response_serializer=daemon__pb2.ReadFileResponse.SerializeToString,
      ),
      'ReadStream': grpc.unary_stream_rpc_method_handler(
          servicer.ReadStream,
          request_deserializer=daemon__pb2.ReadStreamRequest.FromString,
          response_serializer=daemon__pb2.ReadStreamResponse.SerializeToString,
      ),
      'Delete': grpc.unary_unary_rpc_method_handler(
          servicer.Delete,
          request_deserializer=daemon__pb2.DeleteRequest.FromString,
          response_serializer=daemon__pb2.DeleteResponse.SerializeToString,
      ),
      'Check': grpc.unary_unary_rpc_method_handler(
          servicer.Check,
          request_deserializer=daemon__pb2.CheckRequest.FromString,
          response_serializer=daemon__pb2.CheckResponse.SerializeToString,
      ),
      'Repair': grpc.unary_unary_rpc_method_handler(
          servicer.Repair,
          request_deserializer=daemon__pb2.RepairRequest.FromString,
          response_serializer=daemon__pb2.RepairResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'schema.FileService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class MetadataServiceStub(object):
  """MetadataService is used to set, get and delete metadata directly
  using the underlying metadata storage client.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SetMetadata = channel.unary_unary(
        '/schema.MetadataService/SetMetadata',
        request_serializer=daemon__pb2.SetMetadataRequest.SerializeToString,
        response_deserializer=daemon__pb2.SetMetadataResponse.FromString,
        )
    self.GetMetadata = channel.unary_unary(
        '/schema.MetadataService/GetMetadata',
        request_serializer=daemon__pb2.GetMetadataRequest.SerializeToString,
        response_deserializer=daemon__pb2.GetMetadataResponse.FromString,
        )
    self.DeleteMetadata = channel.unary_unary(
        '/schema.MetadataService/DeleteMetadata',
        request_serializer=daemon__pb2.DeleteMetadataRequest.SerializeToString,
        response_deserializer=daemon__pb2.DeleteMetadataResponse.FromString,
        )


class MetadataServiceServicer(object):
  """MetadataService is used to set, get and delete metadata directly
  using the underlying metadata storage client.
  """

  def SetMetadata(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetMetadata(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteMetadata(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MetadataServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SetMetadata': grpc.unary_unary_rpc_method_handler(
          servicer.SetMetadata,
          request_deserializer=daemon__pb2.SetMetadataRequest.FromString,
          response_serializer=daemon__pb2.SetMetadataResponse.SerializeToString,
      ),
      'GetMetadata': grpc.unary_unary_rpc_method_handler(
          servicer.GetMetadata,
          request_deserializer=daemon__pb2.GetMetadataRequest.FromString,
          response_serializer=daemon__pb2.GetMetadataResponse.SerializeToString,
      ),
      'DeleteMetadata': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteMetadata,
          request_deserializer=daemon__pb2.DeleteMetadataRequest.FromString,
          response_serializer=daemon__pb2.DeleteMetadataResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'schema.MetadataService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class DataServiceStub(object):
  """DataService is used write, read, delete, check and repair (processed) data.
  as data can be written to multiple servers and/or be split over multiple chunks,
  some metadata is returned which the user is expected to store somewhere,
  as that metadata is required to read and manage the data, later on.

  Should you not want to have to deal with this metadata yourself,
  you should use the FileService instead, which is one level higher,
  and takes care of managing and storing the metadata for you,
  as well as generating extra metadata, such as the creation epoch time.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Write = channel.unary_unary(
        '/schema.DataService/Write',
        request_serializer=daemon__pb2.DataWriteRequest.SerializeToString,
        response_deserializer=daemon__pb2.DataWriteResponse.FromString,
        )
    self.WriteFile = channel.unary_unary(
        '/schema.DataService/WriteFile',
        request_serializer=daemon__pb2.DataWriteFileRequest.SerializeToString,
        response_deserializer=daemon__pb2.DataWriteFileResponse.FromString,
        )
    self.WriteStream = channel.stream_unary(
        '/schema.DataService/WriteStream',
        request_serializer=daemon__pb2.DataWriteStreamRequest.SerializeToString,
        response_deserializer=daemon__pb2.DataWriteStreamResponse.FromString,
        )
    self.Read = channel.unary_unary(
        '/schema.DataService/Read',
        request_serializer=daemon__pb2.DataReadRequest.SerializeToString,
        response_deserializer=daemon__pb2.DataReadResponse.FromString,
        )
    self.ReadFile = channel.unary_unary(
        '/schema.DataService/ReadFile',
        request_serializer=daemon__pb2.DataReadFileRequest.SerializeToString,
        response_deserializer=daemon__pb2.DataReadFileResponse.FromString,
        )
    self.ReadStream = channel.unary_stream(
        '/schema.DataService/ReadStream',
        request_serializer=daemon__pb2.DataReadStreamRequest.SerializeToString,
        response_deserializer=daemon__pb2.DataReadStreamResponse.FromString,
        )
    self.Delete = channel.unary_unary(
        '/schema.DataService/Delete',
        request_serializer=daemon__pb2.DataDeleteRequest.SerializeToString,
        response_deserializer=daemon__pb2.DataDeleteResponse.FromString,
        )
    self.Check = channel.unary_unary(
        '/schema.DataService/Check',
        request_serializer=daemon__pb2.DataCheckRequest.SerializeToString,
        response_deserializer=daemon__pb2.DataCheckResponse.FromString,
        )
    self.Repair = channel.unary_unary(
        '/schema.DataService/Repair',
        request_serializer=daemon__pb2.DataRepairRequest.SerializeToString,
        response_deserializer=daemon__pb2.DataRepairResponse.FromString,
        )


class DataServiceServicer(object):
  """DataService is used write, read, delete, check and repair (processed) data.
  as data can be written to multiple servers and/or be split over multiple chunks,
  some metadata is returned which the user is expected to store somewhere,
  as that metadata is required to read and manage the data, later on.

  Should you not want to have to deal with this metadata yourself,
  you should use the FileService instead, which is one level higher,
  and takes care of managing and storing the metadata for you,
  as well as generating extra metadata, such as the creation epoch time.
  """

  def Write(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def WriteFile(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def WriteStream(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Read(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReadFile(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReadStream(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Delete(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Check(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Repair(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DataServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Write': grpc.unary_unary_rpc_method_handler(
          servicer.Write,
          request_deserializer=daemon__pb2.DataWriteRequest.FromString,
          response_serializer=daemon__pb2.DataWriteResponse.SerializeToString,
      ),
      'WriteFile': grpc.unary_unary_rpc_method_handler(
          servicer.WriteFile,
          request_deserializer=daemon__pb2.DataWriteFileRequest.FromString,
          response_serializer=daemon__pb2.DataWriteFileResponse.SerializeToString,
      ),
      'WriteStream': grpc.stream_unary_rpc_method_handler(
          servicer.WriteStream,
          request_deserializer=daemon__pb2.DataWriteStreamRequest.FromString,
          response_serializer=daemon__pb2.DataWriteStreamResponse.SerializeToString,
      ),
      'Read': grpc.unary_unary_rpc_method_handler(
          servicer.Read,
          request_deserializer=daemon__pb2.DataReadRequest.FromString,
          response_serializer=daemon__pb2.DataReadResponse.SerializeToString,
      ),
      'ReadFile': grpc.unary_unary_rpc_method_handler(
          servicer.ReadFile,
          request_deserializer=daemon__pb2.DataReadFileRequest.FromString,
          response_serializer=daemon__pb2.DataReadFileResponse.SerializeToString,
      ),
      'ReadStream': grpc.unary_stream_rpc_method_handler(
          servicer.ReadStream,
          request_deserializer=daemon__pb2.DataReadStreamRequest.FromString,
          response_serializer=daemon__pb2.DataReadStreamResponse.SerializeToString,
      ),
      'Delete': grpc.unary_unary_rpc_method_handler(
          servicer.Delete,
          request_deserializer=daemon__pb2.DataDeleteRequest.FromString,
          response_serializer=daemon__pb2.DataDeleteResponse.SerializeToString,
      ),
      'Check': grpc.unary_unary_rpc_method_handler(
          servicer.Check,
          request_deserializer=daemon__pb2.DataCheckRequest.FromString,
          response_serializer=daemon__pb2.DataCheckResponse.SerializeToString,
      ),
      'Repair': grpc.unary_unary_rpc_method_handler(
          servicer.Repair,
          request_deserializer=daemon__pb2.DataRepairRequest.FromString,
          response_serializer=daemon__pb2.DataRepairResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'schema.DataService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
