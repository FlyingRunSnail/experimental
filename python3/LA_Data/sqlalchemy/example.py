#! /usr/bin/env python3
import json
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

import LACityData
import NYCityData
import ORM

if __name__ == "__main__":

    Session = sqlalchemy.orm.sessionmaker(ORM.db)
    session = Session()
    ORM.base.metadata.create_all(ORM.db)

    LALibraryBranches = LACityData.LACityData('a4nt-4gca')
    LALibraryBranches.get_data()
    for library in LALibraryBranches.data:
        #print(library)
        branch = ORM.LALibraryBranches()
        branch.BranchName = library['branch_name']
        branch.PhoneNumber = library['phone_number']
        branch.Email = library['email']
        branch.CouncilDistrict = library['council_district']
        human_address = json.loads(library['location']['human_address'])
        #print(type(human_address))
        #print(human_address)
        #print("Address = {}".format(human_address['address']))
        #print("City = {}".format(human_address['city']))
        #print("State = {}".format(human_address['state']))
        #print("Zip = {}".format(human_address['zip']))
        branch.Address = human_address['address']
        branch.City = human_address['city']
        branch.State = human_address['state']
        branch.Zip = human_address['zip']
        try:
            session.add(branch)
            session.commit()
        except:
            print("Failed On {}".format(library['branch_name']))
            session.rollback()
        del (branch)

    QueensLibraryBranches = NYCityData.NYCityData('swsf-ed7j')
    QueensLibraryBranches.get_data()
    #print(QueensLibraryBranches.data)
    for library in QueensLibraryBranches.data:
        #print(library)
        branch = ORM.QueensLibraryBranches()
        branch.BranchName = library['name']
        branch.PhoneNumber = library['phone']
        branch.Address = library['address']
        branch.City = library['city']
        branch.Zip = library['postcode']
        branch.Burough = library['borough']
        try:
            branch.CommunityCouncil = library['community_council']
        except:
            branch.CommunityCouncil = 0

        try:
            session.add(branch)
            session.commit()
        except:
            session.rollback()
        del (branch)
