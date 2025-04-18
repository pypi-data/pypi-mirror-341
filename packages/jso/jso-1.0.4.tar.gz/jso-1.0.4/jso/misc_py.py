# pylint: disable=no-name-in-module
import datetime
import os

from pydicom import Dataset
from pynetdicom import (
    AE,
    evt,
    debug_logger,
    build_role,
    AllStoragePresentationContexts,
)
from pynetdicom.sop_class import (
    Verification,
    DigitalXRayImageStorageForPresentation,

    PatientRootQueryRetrieveInformationModelGet,
    StudyRootQueryRetrieveInformationModelGet,
    PatientStudyOnlyQueryRetrieveInformationModelGet,

    PatientRootQueryRetrieveInformationModelMove,
    StudyRootQueryRetrieveInformationModelMove,
    PatientStudyOnlyQueryRetrieveInformationModelMove,
)

# debug_logger()

from jso.misc import BaseDicomHandler


class DicomServer(BaseDicomHandler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_server(self):
        self.ae.add_supported_context(Verification)
        self.ae.supported_contexts = AllStoragePresentationContexts
        handlers = [
            (evt.EVT_C_ECHO, self.handle_echo),
            (evt.EVT_C_STORE, self.handle_store),
        ]
        # Start the SCP in non-blocking mode
        self.ae.start_server(
            (self.host, self.port),
            block=self.block,
            evt_handlers=handlers
        )


class DicomClient(BaseDicomHandler):
    store_contexts = [
        DigitalXRayImageStorageForPresentation
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for cx in self.store_contexts:
            self.ae.add_requested_context(cx)

    def QR_Get(self, q_level, **q_kwargs):
        if q_level == 'STUDY':
            query = StudyRootQueryRetrieveInformationModelGet
        elif q_level == 'SERIES':
            query = PatientRootQueryRetrieveInformationModelGet
        else:
            query = PatientStudyOnlyQueryRetrieveInformationModelGet

        self.ae.add_requested_context(query)

        ds = Dataset()
        ds.QueryRetrieveLevel = q_level
        for k, v in q_kwargs.items():
            if hasattr(ds, k):
                setattr(ds, k, v)

        ext_neg = [build_role(cx, scp_role=True) for cx in self.store_contexts]
        handlers = [(evt.EVT_C_STORE, self.handle_store)]
        assoc = self.ae.associate(
            self.host, self.port, ae_title=self.remote_ae_title,
            ext_neg=ext_neg, evt_handlers=handlers
        )
        if assoc.is_established:
            # Use the C-GET service to send the identifier
            responses = assoc.send_c_get(ds, query)
            for (status, _) in responses:
                if status:
                    print('C-GET query status: 0x{0:04x}'.format(status.Status))
                else:
                    raise Exception('DICOM C-GET request timed out')

            # Release the association
            assoc.release()
        else:
            raise Exception('DICOM Server is unavailable')

    def QR_Move(self, q_level, **q_kwargs):
        if q_level == 'STUDY':
            query = StudyRootQueryRetrieveInformationModelMove
        elif q_level == 'SERIES':
            query = PatientRootQueryRetrieveInformationModelMove
        else:
            query = PatientStudyOnlyQueryRetrieveInformationModelMove

        self.ae.add_requested_context(query)

        ds = Dataset()
        ds.QueryRetrieveLevel = q_level
        for k, v in q_kwargs.items():
            setattr(ds, k, v)

        assoc = self.ae.associate(
            self.host, self.port, ae_title=self.remote_ae_title,
        )
        if assoc.is_established:
            responses = assoc.send_c_move(ds, self.ae_title, query)
            for (status, _) in responses:
                if status:
                    print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
                else:
                    print(f'C-MOVE query timeout: {q_kwargs}')
                    raise Exception('DICOM C-MOVE request timed out')

            # Release the association
            assoc.release()
        else:
            raise Exception('DICOM Server [%s@%s:%s] is unavailable.'.format(
                self.remote_ae_title, self.host, self.port))


if __name__ == '__main__':
    DicomClient(
        host='88.20.10.141', port=4002, remote_ae_title='jhbfz_storeQR'
    ).QR_Move(
        'STUDY',
        StudyInstanceUID='1.2.840.113619.2.261.4.2147483647.20241127.385431'
    )
