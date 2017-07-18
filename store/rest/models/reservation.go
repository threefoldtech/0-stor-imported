package models

import (
	"encoding/binary"
	"fmt"
	"time"

	"github.com/zero-os/0-stor/store/goraml"

	"strings"

	"github.com/zero-os/0-stor/store/db"
	"github.com/zero-os/0-stor/store/utils"
	validator "gopkg.in/validator.v2"
)

var _ (db.Model) = (*Reservation)(nil)

/*
-----------------------------------------------------------------
SizeReserved| TotalSizeReserved |Size of CreationDate
 8         |   8                |  2
-----------------------------------------------------------------

-----------------------------------------------------------------------
Size of UpdateDate     |Size of ExpirationDate | Size ID | Size AdminID
    2                  |         2             |  2       |   2
----------------------------------------------------------------------

------------------------------------------------------------
 CreationDate | UpdateDate | ExpirationDate | ID | AdminId
------------------------------------------------------------

*/

type Reservation struct {
	Namespace    string
	AdminId      string          `json:"adminId" validate:"regexp=^[a-zA-Z0-9]+$,nonzero"`
	Created      goraml.DateTime `json:"created" validate:"nonzero"`
	ExpireAt     goraml.DateTime `json:"expireAt" validate:"nonzero"`
	Id           string          `json:"id" validate:"regexp=^[a-zA-Z0-9]+$,nonzero"`
	SizeReserved float64         `json:"sizeReserved" validate:"min=1,multipleOf=1,nonzero"`
	SizeUsed     float64         `json:"sizeUsed" validate:"min=1,nonzero"`
	Updated      goraml.DateTime `json:"updated" validate:"nonzero"`
}

func NewReservation(namespace string, admin string, size float64, period int) (*Reservation, error) {
	creationDate := time.Now()
	expirationDate := creationDate.AddDate(0, 0, period)

	uuid, err := utils.GenerateUUID(64)

	if err != nil {
		return nil, err
	}

	return &Reservation{
		Namespace:    namespace,
		AdminId:      admin,
		SizeReserved: size,
		SizeUsed:     0,
		ExpireAt:     goraml.DateTime(expirationDate),
		Created:      goraml.DateTime(creationDate),
		Updated:      goraml.DateTime(creationDate),
		Id:           uuid,
	}, nil
}

func (s Reservation) Validate() error {
	return validator.Validate(s)
}

func (s Reservation) SizeRemaining() float64 {
	return s.SizeReserved - s.SizeUsed
}

func (s Reservation) Key() string {
	label := s.Namespace
	if strings.Index(label, NAMESPACE_PREFIX) != -1 {
		label = strings.Replace(label, NAMESPACE_PREFIX, "", 1)
	}
	return fmt.Sprintf("%s%s_%s", RESERVATION_PREFIX, label, s.Id)
}

func (s Reservation) Encode() ([]byte, error) {

	adminId := s.AdminId
	aSize := int16(len(adminId))

	id := s.Id
	iSize := int16(len(id))

	created := []byte(time.Time(s.Created).Format(time.RFC3339))
	updated := []byte(time.Time(s.Updated).Format(time.RFC3339))
	expiration := []byte(time.Time(s.ExpireAt).Format(time.RFC3339))

	cSize := int16(len(created))
	uSize := int16(len(updated))
	eSize := int16(len(expiration))

	result := make([]byte, 26+cSize+uSize+eSize+aSize+iSize)

	copy(result[0:8], utils.Float64bytes(s.SizeReserved))
	copy(result[8:16], utils.Float64bytes(s.SizeUsed))

	binary.LittleEndian.PutUint16(result[16:18], uint16(cSize))
	binary.LittleEndian.PutUint16(result[18:20], uint16(uSize))
	binary.LittleEndian.PutUint16(result[20:22], uint16(eSize))
	binary.LittleEndian.PutUint16(result[22:24], uint16(iSize))
	binary.LittleEndian.PutUint16(result[24:26], uint16(aSize))

	//Creation Date size and date
	start := 26
	end := 26 + cSize
	copy(result[start:end], created)

	//update Date
	start2 := end
	end2 := end + uSize
	copy(result[start2:end2], updated)

	//ExpirationDate
	start3 := end2
	end3 := start3 + eSize
	copy(result[start3:end3], expiration)

	// ID
	start4 := end3
	end4 := start4 + iSize
	copy(result[start4:end4], []byte(id))

	// Admin ID
	start5 := end4
	end5 := start5 + aSize
	copy(result[start5:end5], []byte(adminId))
	return result, nil
}

func (s *Reservation) Decode(data []byte) error {
	s.SizeReserved = utils.Float64frombytes(data[0:8])
	s.SizeUsed = utils.Float64frombytes(data[8:16])

	cSize := int16(binary.LittleEndian.Uint16(data[16:18]))
	uSize := int16(binary.LittleEndian.Uint16(data[18:20]))
	eSsize := int16(binary.LittleEndian.Uint16(data[20:22]))
	iSize := int16(binary.LittleEndian.Uint16(data[22:24]))
	aSize := int16(binary.LittleEndian.Uint16(data[24:26]))

	start := 26
	end := 26 + cSize

	cTime, err := time.Parse(time.RFC3339, string(data[start:end]))

	if err != nil {
		return err
	}

	start2 := end
	end2 := end + uSize

	uTime, err := time.Parse(time.RFC3339, string(data[start2:end2]))

	if err != nil {
		return err
	}

	start3 := end2
	end3 := end2 + eSsize

	eTime, err := time.Parse(time.RFC3339, string(data[start3:end3]))

	if err != nil {
		return err
	}

	start4 := end3
	end4 := start4 + iSize

	start5 := end4
	end5 := start5 + aSize

	s.Created = goraml.DateTime(cTime)
	s.Updated = goraml.DateTime(uTime)
	s.ExpireAt = goraml.DateTime(eTime)

	s.Id = string(data[start4:end4])
	s.AdminId = string(data[start5:end5])
	return nil
}
