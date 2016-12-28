import pandas as pd
import glob
import os


if __name__ == '__main__':

	path = 'ministerio_agricultura'

	files = [f for f in glob.glob("_data/%s/*.csv" % path) if os.path.isfile(f)]
	for f in files:
		_data = pd.read_csv('%s' % f, encoding='utf-8')
		_data.drop(_data.columns[[0]], axis=1, inplace=True)
		_f = f.split("/")[-1]
		if not os.path.exists("_data/f_%s" % path):
			os.mkdir("_data/f_%s" % path,0755);
		_data.to_csv('_data/f_%s/%s' % (path, _f), sep=',', encoding='utf-8', index=False, header=False)