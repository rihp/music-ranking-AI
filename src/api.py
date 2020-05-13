import flask, argparse

def parserFunction():
    # 02 - INSTRUCTIONS AND ARGUMENTS
    parser = argparse.ArgumentParser(description="Vesuvius is a retriever of satellite images. It currently uses a dataset containing volcanic eruptions and matches it with available photos from NASA's DSCOVR satellite, using the 'EPIC' API. The functionality of vesuvius has been desinged to be a modular program, in the sense that one could input a different dataset with relevant dates, and get the available satellite images from that date; Note that the DSCOVR satellite was launched into space on 2015, so older data will not be available. Also, very recent dates may not be available in the API's archive. DISCLAIMER: Use at your own risk.")
    parser.add_argument('lat', help="required latitude point to query. Type: float")
    parser.add_argument('lng', help="required latitude point to query. Type: float")
    parser.add_argument('--radius', help="Functionality under development; sets the radius to apply to the query.")
    parser.add_argument('--mailto', help="sends an email to the specified email.")
    parser.add_argument('--address', help="Not yet developed.")
    #parser.add_argument('--version', help="displays vesuvius' version", )

    # 03 -PARSE ARGS AND CATCH ERRORS, like wrong lengths or formats
    args = parser.parse_args()
    """
    if type(longitude) is not float:
        print(type(longitude))
        raise ValueError('latitude must be a float')
    if args.lng is not float: # | (int(args.month) > 12)):
        print(type(longitude))
        raise ValueError('longitude must be a float')
    """
    return args
args = parserFunction()
latitude = float(args.lat)
longitude = float(args.lng)